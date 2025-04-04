import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.bot.routers import router
from src.logger.logger import setup_logger
from src.settings.settings import settings

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))


async def main():
    # логирование
    setup_logger()

    # планировщик для отправки нотификаций
    # scheduler = AsyncIOScheduler()
    # scheduler.add_job(check_and_send_notifications, "interval", minutes=1)
    # scheduler.start()

    # телеграм бот
    bot = Bot(token=settings.bot.token)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)

    # запуск бота
    logging.info("Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
