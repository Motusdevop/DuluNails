from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


class Menu():
    _button_appointment = KeyboardButton(text='Записаться на процедуру 💅')
    _button_portfolio = KeyboardButton(text='Посмотреть портфолио 💫')
    _button_prices = KeyboardButton(text='Прайс-лист 💸')
    _button_my_windows = KeyboardButton(text='Мои записи 🌿️️️️️️')

    _kb = [[_button_appointment], [_button_portfolio, _button_prices], [_button_my_windows]]

    markup = ReplyKeyboardMarkup(keyboard=_kb, resize_keyboard=True)

class Admin():
    _kb = [
        [KeyboardButton(text='Посмотреть записи')],
        [KeyboardButton(text='Добавить окно'), KeyboardButton(text='Бан-лист')],
        [KeyboardButton(text='Сделать рассылку'), KeyboardButton(text='Посмотреть логи')]
    ]
    markup = ReplyKeyboardMarkup(keyboard=_kb, resize_keyboard=True)

class Confirm():
    _kb = [[InlineKeyboardButton(text='Принять', callback_data='1'),
            InlineKeyboardButton(text='Отменить', callback_data='0')]]

    markup = InlineKeyboardMarkup(inline_keyboard=_kb)


class Contact():
    kb = [[KeyboardButton(text='Отправить свой контакт ☎️', request_contact=True)]]

    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
