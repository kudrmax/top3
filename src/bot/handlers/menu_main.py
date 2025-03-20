from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.complete_plan import complete_plan
from src.bot.handlers.create_plan import try_create_daily_plan
from src.bot.handlers.get_plan import get_plan
from src.bot.keyboards import main_kb

router = Router()


async def start_main_menu_pipeline(
        message: Message,
        state: FSMContext,
):
    await message.answer(
        "Нажмите кнопку",
        reply_markup=main_kb()
    )
    await state.clear()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await start_main_menu_pipeline(message, state)


@router.message(StateFilter(None), F.text.lower().contains('посмотреть'))
async def get(message: Message, state: FSMContext):
    await get_plan(message, state)


@router.message(StateFilter(None), F.text.lower().contains('создать'))
async def create(message: Message, state: FSMContext):
    await try_create_daily_plan(message, state)


@router.message(StateFilter(None), F.text.lower().contains('подтвердить'))
async def complete(message: Message, state: FSMContext):
    await complete_plan(message, state)
