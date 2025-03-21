from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.plans.complete import complete_plan
from src.bot.handlers.plans.create import try_create_daily_plan
from src.bot.handlers.plans.get import get_plan
from src.bot.handlers.texsts import Texts
from src.bot.keyboards import main_kb
from src.models.user import User

router = Router()


async def start_main_menu_pipeline(
        message: Message,
        state: FSMContext,
):
    kb = main_kb(User(message))
    await message.answer(
        Texts.start,
        reply_markup=kb,
    )
    await message.answer(
        "Нажмите кнопку",
        reply_markup=kb,
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


@router.message(StateFilter(None), F.text.lower().contains('изменить'))
async def update(message: Message, state: FSMContext):
    await message.answer(Texts.not_implemented)


@router.message(StateFilter(None), F.text.lower().contains('сообщить'))
async def report(message: Message, state: FSMContext):
    await message.answer(Texts.report_bug_to_max)
