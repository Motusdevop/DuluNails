from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, Message

from keyboards import menu
from forms.register import RegisterForm

from repository import UserRepository

router = Router()

@router.message(RegisterForm.phone)
async def register(message: Message, state: FSMContext):
    contact = message.contact

    username = contact.first_name + ' ' + contact.last_name if contact.last_name else contact.first_name
    telegram_id = contact.user_id
    phone = contact.phone_number

    UserRepository.register_user(username=username, telegram_id=telegram_id, phone=phone)
    await message.answer(
        'Успешно', reply_markup=menu.markup
    )