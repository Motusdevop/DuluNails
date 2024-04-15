from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, \
    FSInputFile

import keyboards
from repository import UserRepository

from forms.register import RegisterForm

from keyboards import Menu, Contact, Admin

router = Router()


async def check_register(message: Message, state: FSMContext):
    if not UserRepository.check_register(message.from_user.id):
        kb = [[KeyboardButton(text='Отправить свой контакт ☎️', request_contact=True)]]
        markup = ReplyKeyboardMarkup(keyboard=kb)

        await message.answer(
            'Пожалуйста сначала зарегистрируйтесь. Для этого нажмите кнопку: "Отправить свой контакт ☎️"',
                             reply_markup=Contact.markup)
        await state.set_state(RegisterForm.phone)


@router.message(F.text, CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(
        """Здравствуйте, это бот для записи на маникюр""",
        reply_markup=Menu.markup, parse_mode=ParseMode.MARKDOWN
    )
    await check_register(message, state)

@router.message(F.text, Command('admin'))
async def admin_panel(message: Message, state: FSMContext):
    await message.answer('Здравствуйте', reply_markup=Admin.markup)

@router.message(F.text.lower() == 'прайс-лист 💸')
async def pricelist(message: Message):
    photo = FSInputFile("media/pricelist.jpg")
    await message.answer_photo(photo=photo, caption='Актуальный прайслист')

@router.message(F.text.lower() == 'посмотреть портфолио 💫')
async def portfolio(message: Message):
    await message.answer('Портфолио в канале @dulullu')

