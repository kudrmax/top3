from aiogram import Router

from src.bot.handlers.errors import router as error_handlers
from src.bot.handlers.menus.menu_main import router as menu_main

from src.bot.handlers.pipelines.create import router as create
from src.bot.handlers.pipelines.get import router as get
from src.bot.handlers.pipelines.complete import router as complete

router = Router()

router.include_routers(
    error_handlers,
    menu_main,
    create,
    complete,
    get,
)
