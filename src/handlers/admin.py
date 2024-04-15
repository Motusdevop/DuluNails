from aiogram import Router

router = Router()

@router.message(F.text)
async def cmd_start(message: Message):
    await message.answer(
        """Здравствуйте, это бот для записи на маникюр""", reply_markup=menu,parse_mode=ParseMode.MARKDOWN
    )