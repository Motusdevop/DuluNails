from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram.types import FSInputFile

from repository import UserRepository

from forms.register import RegisterForm

from keyboards import Menu, Contact, Admin

from config import settings

router = Router()



async def check_register(message: Message, state: FSMContext):
    if not UserRepository.check_register(message.from_user.id):
        await message.answer(
            'Пожалуйста сначала зарегистрируйтесь. Для этого нажмите кнопку: "Отправить свой контакт ☎️"',
                             reply_markup=Contact.markup)
        await state.set_state(RegisterForm.phone)
        return False
    return True


@router.message(F.text, CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        """Здравствуйте, это бот для записи на маникюр""",
        reply_markup=Menu.markup, parse_mode=ParseMode.MARKDOWN
    )
    await check_register(message, state)

@router.message(F.text, Command('about'))
async def about(message: Message):
    await message.answer(
"""Привет! Меня зовут Света, и этот бот создан для удобства записи ко мне на процедуру 💅

🧘🏼‍♀️С помощью него вы сможете: посмотреть актуальный прайс-лист, мое портфолио, записаться на маникюр и получить рассылку о свободных окнах. 
🧘🏼‍♀️В скором времени мы добавим систему акций, чтобы приходить ко мне было еще приятней."""
    )

@router.message(F.text, Command('admin'))
async def admin_panel(message: Message, state: FSMContext):
    if message.from_user.id in settings.admins:
        await message.answer('Здравствуйте', reply_markup=Admin.markup)
    else:
        pass

@router.message(F.text.lower() == 'прайс-лист 💸')
async def pricelist(message: Message):
    photo = FSInputFile("media/pricelist.jpg")
    await message.answer_photo(photo=photo, caption='Актуальный прайс-лист')

@router.message(F.text.lower() == 'посмотреть портфолио 💫')
async def portfolio(message: Message):
    await message.answer('Портфолио в канале @dulullu')

