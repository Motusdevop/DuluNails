import asyncio
from aiogram import Bot, Dispatcher

from handlers.base import router as base_router
from handlers.appointment import router as appointment_router
from handlers.register import router as register_router
from handlers.admin import router as admin_router

from database import create_tables

from config import settings

# Запуск бота
async def main():
    bot = Bot(token=settings.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(base_router, appointment_router, register_router, admin_router)

    await bot.delete_webhook(drop_pending_updates=True)
    create_tables()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())