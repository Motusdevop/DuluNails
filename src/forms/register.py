from aiogram.fsm.state import StatesGroup, State


class RegisterForm(StatesGroup):
    begin = State()
    phone = State()