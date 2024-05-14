import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

import keyboards
from forms.approintment_forms import MakeApprointmentForm

from aiogram.enums import ParseMode

from repository import WindowRepository, UserRepository
from handlers.base import check_register

from config import settings

router = Router()

@router.message(F.text.lower() == 'записаться на процедуру 💅')
async def appointment(message: Message, state: FSMContext):
    if await check_register(message, state):
        user = UserRepository.get_user(message.from_user.id)
        if not user.is_banned:
            windows = WindowRepository.get_all_no_active_windows()

            if len(windows) == 0:
                await message.answer('Доступных окон нет')
                await state.clear()

            else:
                await state.set_state(MakeApprointmentForm.correct_time)
                kb = list()

                for i in range(len(windows)):
                    window = windows[i]
                    kb.append(
                        [InlineKeyboardButton(text=f'{i+1}. {window.datetime_to_str(window.datetime)}',
                                                    callback_data=f'{window.id}')])

                    markup = InlineKeyboardMarkup(inline_keyboard=kb)

                await message.answer('Пожалуйста выберите удобное для вас дату', reply_markup=markup)
        else:
            await message.answer('Вы не можете записаться так как вы получили блокировку, для разблокировки напишите: @svessin')

@router.message(F.text.lower() == 'мои записи 🌿️️️️️️')
async def portfolio(message: Message, state: FSMContext):
    if await check_register(message, state):
        windows = WindowRepository.all_window_per_user(message.from_user.id)
        if len(windows) == 0:
            await message.answer('У вас нету активных записей')
        else:
            await message.answer('Ваши записи:')
            for i in range(len(windows)):
                text = f'''
{i+1}. *{windows[i].datetime_to_str(windows[i].datetime)} в {str(windows[i].correct_time)[:-3]}*
'''
                await message.answer(text, parse_mode=ParseMode.MARKDOWN)
            await message.answer('Для отмены записи или переноса, за *24 часа* напишите: @svessin',
                                 parse_mode=ParseMode.MARKDOWN)
@router.callback_query(MakeApprointmentForm.correct_time)
async def correct_time(callback: CallbackQuery, state: FSMContext):
    try:
        window_id = callback.data

        data = {'window_id': window_id, 'active': True, 'user_id': callback.from_user.id}

        window = WindowRepository.get_window(int(window_id))

        await state.update_data(**data)
        await state.set_state(MakeApprointmentForm.window_id)

        await callback.message.delete()

        await callback.message.answer(f'Введите удобное вам время {window.datetime_to_str(window.datetime)} до 20:00 в формате "часы:минуты"')
    except ValueError:
        await state.clear()

@router.message(MakeApprointmentForm.window_id)
async def select_window(message: Message, state: FSMContext):
    try:
        data = await state.get_data()

        window = WindowRepository.get_window(int(data['window_id']))

        msg = message.text.split(':')
        user_time = datetime.time(hour=int(msg[0]), minute=int(msg[1]))
        flag = False

        if window.datetime.hour < user_time.hour < 20:
            flag = True

        elif window.datetime.hour == user_time.hour < 20:
            if window.datetime.minute <= user_time.minute:
                flag = True

        elif window.datetime.hour < user_time.hour == 20:
            if user_time.minute == 0:
                flag = True

        if flag:
            await state.update_data(correct_time=user_time)
            await state.set_state(MakeApprointmentForm.confirmation)
            await message.answer(f'''
*Вы выбрали окно {window.datetime_to_str(window.datetime)} в {message.text} вы уверены?*
В случае если вы не придёте на процедуру, то вы получите блокировку, для разблокировки нужно будет заплатить штраф
Для переноса времени свяжитесь с мастером @svessin''',
                                          reply_markup=keyboards.Confirm.markup, parse_mode=ParseMode.MARKDOWN)
        else:
            await message.answer('Вы вышли за границы окна, запишитесь заново')
            await state.clear()
    except:
        await message.answer('Неверный формат запишитесь заново')
        await state.clear()

@router.callback_query(MakeApprointmentForm.confirmation)
async def confirm_appointment(callback: CallbackQuery, state: FSMContext):
    if callback.data == '1':

        data = await state.get_data()

        window_id = data['window_id']

        user = UserRepository.get_user(int(data['user_id']))

        try:
            WindowRepository.update_window(int(window_id), data)
            window = WindowRepository.get_window(window_id)
            await callback.message.answer('''
Успешно, процедура будет проходить по адресу: 
`Москва, улица Россошанская, дом 6, подъезд 4`
Домофон: 220, Этаж: 8 для дополнительной информации: @svessin''', parse_mode=ParseMode.MARKDOWN)
            await callback.message.answer_location(55.59230848008093, 37.61215122188916)

            text = f'Окно: {window.datetime_to_str(window.datetime)} было занято: @{user.username} конкретное время: {window.correct_time}'
            for admin in settings.admins:
                await callback.bot.send_message(admin, text)

            await callback.message.delete()

        except:
            await state.clear()
            await callback.answer('Что-то пошло не так попробуйте позже')

    elif callback.data == '0':
        await callback.message.delete()
        await callback.message.answer('Запись не создана')

    await state.clear()