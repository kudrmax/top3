import logging

from aiogram import Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ErrorEvent
from requests.exceptions import ConnectionError

from src.bot.keyboards import main_kb
from src.models.user import User

router = Router()


async def go_to_main_menu_after_error(event: ErrorEvent, state: FSMContext):
    logger = logging.getLogger(__name__)
    if event.update.message:
        await event.update.message.answer(
            f"Oops, something went wrong!",
            reply_markup=main_kb(User(event.update.message)),
        )
    logger.error(f"Unhandled exception: {event.exception}")
    await state.clear()


@router.errors(ExceptionTypeFilter(ConnectionError))
async def connection_error(event: ErrorEvent, state: FSMContext):
    await event.update.message.answer(f"Can't connect to server.")
    await go_to_main_menu_after_error(event, state)


@router.errors()
async def all_errors(event: ErrorEvent, state: FSMContext):
    await go_to_main_menu_after_error(event, state)
