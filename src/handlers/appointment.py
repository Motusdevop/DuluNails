from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from forms.approintment_forms import CreateApprointmentForm

router = Router()

@router.message(F.text.lower() == 'записаться на процедуру 💅')
async def appointment(message: Message, state: FSMContext):
    await state.set_state(CreateApprointmentForm.approiment_id)
    await message.answer('окей')

