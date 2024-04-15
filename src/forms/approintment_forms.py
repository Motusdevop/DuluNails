from aiogram.fsm.state import StatesGroup, State


class CreateApprointmentForm(StatesGroup):
    approiment_id = State()
    service_id = State()
    confirmation = State()