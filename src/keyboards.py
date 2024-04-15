from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class Menu():
    _button_appointment = KeyboardButton(text='Записаться на процедуру 💅')
    _button_portfolio = KeyboardButton(text='Посмотреть портфолио 💫')
    _button_prices = KeyboardButton(text='Прайс-лист 💸')

    _kb = [[_button_appointment], [_button_portfolio, _button_prices]]

    markup = ReplyKeyboardMarkup(keyboard=_kb, resize_keyboard=True)

class Admin():
    _kb = [
        [KeyboardButton(text='Посмотреть записи')],
        [KeyboardButton(text='Добавить окна'), KeyboardButton(text='Бан-лист')],
        [KeyboardButton(text='Сделать рассылку'), KeyboardButton(text='Посмотреть логи')],
        [KeyboardButton(text='/start')]
    ]
    markup = ReplyKeyboardMarkup(keyboard=_kb, resize_keyboard=True)


class Contact():
    kb = [[KeyboardButton(text='Отправить свой контакт ☎️', request_contact=True)]]

    markup = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
