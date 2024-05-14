from aiogram.fsm.state import StatesGroup, State


class MakeApprointmentForm(StatesGroup):
    window_id = State()
    correct_time = State()
    confirmation = State()