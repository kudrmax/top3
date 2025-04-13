import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from src.bot.routers import router
from src.logger.logger import setup_logger
from src.services.reminders.reminder_service import ReminderService
from src.services.reminders.reminder_settings_service import reminder_settings_service
from src.settings.settings import settings

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))


async def main():
    # логирование
    setup_logger()

    # телеграм бот
    bot = Bot(token=settings.bot.token)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)

    # настройка уведомлений
    reminder_service = ReminderService(
        reminder_settings_service=reminder_settings_service,
        bot=bot
    )
    dp["reminder_service"] = reminder_service

    # запуск бота
    logging.info("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
