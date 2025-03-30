import datetime as dt

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.functions.plans.get_current_plan_text import get_current_plan_text
from src.bot.functions.plans.get_plans_text import get_plan_text
from src.bot.functions.style import b
from src.bot.handlers.texsts import Texts
from src.bot.keyboards import main_kb, create_plan_kb
from src.common.date_and_time import get_today
from src.errors.base_exception import MyException
from src.models.daily_plan import DailyPlan
from src.models.user import User
from src.services.plans.service import daily_plans_service

router = Router()


async def get_plan(message: Message, state: FSMContext):
    plan_text = get_current_plan_text(User(message))
    if plan_text is None:
        await message.answer(
            Texts.plan_is_not_created,
            reply_markup=create_plan_kb()
        )
    else:
        await message.answer(
            plan_text,
            reply_markup=main_kb(User(message)),
            parse_mode=ParseMode.HTML
        )
