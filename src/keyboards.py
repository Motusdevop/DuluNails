from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class menu():
    _button_appointment = KeyboardButton(text='Записаться на процедуру 💅')
    _button_portfolio = KeyboardButton(text='Посмотреть портфолио 💫')
    _button_prices = KeyboardButton(text='Прайс-лист 💸')

    _kb = [[_button_appointment], [_button_portfolio, _button_prices]]

    markup = ReplyKeyboardMarkup(keyboard=_kb)
