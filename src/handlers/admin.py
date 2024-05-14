from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from forms.admin_forms import AddWindow, DeleteWindow, Mailing, CancelWindow

from models import Window

from exceptions import UncorrectFormat

from repository import WindowRepository, UserRepository

from config import settings

from asyncio import sleep

from exceptions import UserNotFound

import keyboards

router = Router()

@router.message(F.text.lower() == 'добавить окно')
async def add_window(message: Message, state: FSMContext):
    if message.from_user.id in settings.admins:
        await state.set_state(AddWindow.datetime)

        await message.answer(
            'Введите дату и время в формате "число.месяц часы:минуты" например: `28.04 16:30`',
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        pass



@router.message(AddWindow.datetime)
async def datetime(message: Message, state: FSMContext):

    if message.from_user.id in settings.admins:
        try:
            datetime = Window.str_to_datetime(message.text)
            window = Window(datetime=datetime)
            await state.update_data(window=window)
            await message.answer(f'{window.datetime_to_str(window.datetime)} вы уверены?',
                                 reply_markup=keyboards.Confirm.markup)
            await state.set_state(AddWindow.confirm)
        except UncorrectFormat:
            await state.clear()
            await message.answer('Неверный формат')
    else:
        pass



@router.callback_query(AddWindow.confirm)
async def confirm(callback: CallbackQuery, state: FSMContext):

    if callback.data == '1':

        data = await state.get_data()

        WindowRepository.create_window(data['window'])

        await callback.answer('Окно добавлено')
        await callback.message.delete()
        await state.clear()

    else:
        await callback.answer('Окно не добавлено')
        await callback.message.delete()
        await state.clear()


@router.message(F.text.lower() == 'посмотреть записи')
async def get_windows(message: Message, state: FSMContext):
    if message.from_user.id in settings.admins:
        windows = WindowRepository.get_all_windows()

        if len(windows) == 0:
            await message.answer('Записей нет')

        else:
            for window in windows:
                if window.active:
                    user = UserRepository.get_user(window.user_id)
                    text = f'''
        {window.id}: *{window.datetime_to_str(window.datetime)}* в *{str(window.correct_time)[:-3]}*
ЗАНЯТО: {user.fullname} @{user.username}
Номер телефона: +{user.phone}
'''
                    _kb = [[InlineKeyboardButton(text='Удалить', callback_data=f'delete {window.id}'), InlineKeyboardButton(
                        text='Отменить', callback_data=f'cancel {window.id}'
                    )]]
                else:
                    text = f'{window.id}. {window.datetime_to_str(window.datetime)} НЕ ЗАНЯТО'

                    _kb = [[InlineKeyboardButton(text='Удалить', callback_data=f'delete {window.id}')]]

                markup = InlineKeyboardMarkup(inline_keyboard=_kb)
                await message.answer(text, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    else:
        pass

@router.callback_query('delete' == F.data.split()[0])
async def delete_window(callback: CallbackQuery, state: FSMContext):
    try:
        window_id = callback.data.split()[-1]
        window = WindowRepository.get_window(int(window_id))
        await state.set_state(DeleteWindow.confirm)
        await state.update_data(window_id=window_id)
        if window.active:
            text = f'''
Вы уверены что хотите удалить окно номер {window_id}? Дата: {window.datetime_to_str(window.datetime)}
Внимание данное окно уже занято пользователь получит уведомление об этом'''
        else:
            text = f'''
Вы уверены что хотите удалить окно номер {window_id}? Дата: {window.datetime_to_str(window.datetime)}'''

        markup = keyboards.Confirm.markup
        await callback.message.answer(text, reply_markup=markup)
    except AttributeError:
        await callback.message.answer('Это окно уже удалено')

@router.callback_query('cancel' == F.data.split()[0])
async def cancel_window(callback: CallbackQuery, state: FSMContext):
    window_id = callback.data.split()[-1]
    window = WindowRepository.get_window(int(window_id))
    if window.active:
        await state.set_state(CancelWindow.confirm)
        await state.update_data(window_id=window_id)
        text = f'''
Вы уверены что хотите отменить запись на окно номер {window_id}? Дата: {window.datetime_to_str(window.datetime)}
Внимание данное окно уже занято пользователь получит уведомление об этом'''

        markup = keyboards.Confirm.markup
        await callback.message.answer(text, reply_markup=markup)
    else:
        await callback.message.answer('Это окно уже отменено')

@router.callback_query(DeleteWindow.confirm)
async def confirm2(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    if callback.data == '1':
        window = WindowRepository.get_window(data['window_id'])


        if window.active:
            await callback.bot.send_message(window.user_id, '''К сожалению, ваша запись отменена.
Пожалуйста, подберите другое время или свяжитесь по этому юзернейму @svessin''')
        WindowRepository.delete_window(data['window_id'])
        await callback.answer('Окно удалено')
        await callback.message.delete()
        await state.clear()
    else:
        await callback.answer('Окно не удалено')
        await callback.message.delete()
        await state.clear()

@router.callback_query(CancelWindow.confirm)
async def confirm3(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    if callback.data == '1':
        window = WindowRepository.get_window(data['window_id'])


        await callback.bot.send_message(window.user_id, '''К сожалению, ваша запись отменена.
Пожалуйста, подберите другое время или свяжитесь по этому юзернейму @svessin''')
        WindowRepository.cancel_window(data['window_id'])
        await callback.answer('Окно отменено')
        await callback.message.delete()
        await state.clear()
    else:
        await callback.answer('Окно не удалено')
        await callback.message.delete()
        await state.clear()

@router.message(F.text.lower() == 'бан-лист')
async def ban_list(message: Message, state: FSMContext):
    if message.from_user.id in settings.admins:
        banned = UserRepository.get_all_banned()

        await message.answer('Список забаненных пользователей:')
        if len(banned) == 0:
            await message.answer('Забаненных пользователей нет')
        for user in banned:
            await message.answer(f'{user.fullname} @{user.username} время: {user.ban_datetime}')

@router.message(Command('ban'))
async def ban(message: Message, command: CommandObject):
    if message.from_user.id in settings.admins:
        username = command.args[1:]
        if command.args[0] != '@':
            await message.answer('Username должен начинатся с @')
        else:
            try:
                UserRepository.ban(username)

                await message.answer(f'Пользователь @{username} был забанен')
            except UserNotFound:
                await message.answer(f'Пользователь @{username} НЕ НАЙДЕН')


@router.message(Command('unban'))
async def ban(message: Message, command: CommandObject):
    if message.from_user.id in settings.admins:
        username = command.args[1:]
        if command.args[0] != '@':
            await message.answer('Username должен начинатся с @')
        else:
            try:
                UserRepository.unban(username)

                await message.answer(f'Пользователь @{username} был разбанен')
            except UserNotFound:
                await message.answer(f'Пользователь @{username} НЕ НАЙДЕН')

@router.message(F.text.lower() == 'сделать рассылку')
async def mailing(message: Message, state: FSMContext):
    if message.from_user.id in settings.admins:
        await message.answer('Введите сообщение для пользователей')
        await state.set_state(Mailing.get_message)

@router.message(Mailing.get_message)
async def pre_push_mailing(message: Message, state: FSMContext):
    await message.forward(message.from_user.id, message.message_thread_id)
    await state.update_data(message=message)
    await state.set_state(Mailing.confirm)
    await message.answer('Вы уверены', reply_markup=keyboards.Confirm.markup)

@router.callback_query(Mailing.confirm)
async def confirm_mailing(callback: CallbackQuery, state: FSMContext):
    if callback.data == '1':
        data = await state.get_data()
        message: Message = data['message']
        telegram_id_list = UserRepository.get_all_telegram_id()

        await callback.message.answer('Рассылка запущена')
        await callback.message.delete()
        for chat_id in telegram_id_list:
            await message.forward(chat_id, message.message_thread_id)
            await sleep(3)

    elif callback.data == '0':
        await callback.message.answer('Рассылка не была запущена')
        await callback.message.delete()

    await state.clear()

