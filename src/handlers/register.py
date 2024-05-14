from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import Menu
from forms.register import RegisterForm

from repository import UserRepository

router = Router()

@router.message(RegisterForm.phone)
async def register(message: Message, state: FSMContext):
    contact = message.contact

    if contact:

        fullname = contact.first_name + ' ' + contact.last_name if contact.last_name else contact.first_name
        username = message.from_user.username
        telegram_id = contact.user_id
        phone = contact.phone_number

        UserRepository.register_user(fullname=fullname, username=username, telegram_id=telegram_id, phone=phone)
        await message.answer(
            'Вы успешно зарегистровались, спасибо ✅', reply_markup=Menu.markup
        )

    await state.clear()