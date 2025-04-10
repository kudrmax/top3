from aiogram import Router

from src.bot.handlers.errors import router as error_handlers
from src.bot.handlers.menu_main import router as menu_main

from src.bot.handlers.plans.create import router as create
from src.bot.handlers.plans.update import router as update
from src.bot.handlers.plans.get import router as get
from src.bot.handlers.plans.complete import router as complete

router = Router()

router.include_routers(
    error_handlers,
    menu_main,
    create,
    update,
    complete,
    get,
)
