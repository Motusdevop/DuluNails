from aiogram.fsm.state import StatesGroup, State


class AddWindow(StatesGroup):
    datetime = State()
    confirm = State()

class DeleteWindow(StatesGroup):
    confirm = State()

class CancelWindow(StatesGroup):
    confirm = State()

class Mailing(StatesGroup):
    get_message = State()
    confirm = State()
