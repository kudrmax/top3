import datetime as dt

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.functions.style import b
from src.bot.handlers.texsts import Texts
from src.bot.keyboards import main_kb, create_plan_kb
from src.models.daily_plan import DailyPlan
from src.models.user import User
from src.services.plans.service import daily_plans_service

router = Router()


async def get_plan(message: Message, state: FSMContext):
    plan = daily_plans_service.get_current(User(message))
    if plan is None:
        await message.answer(
            Texts.plan_is_not_created,
            reply_markup=create_plan_kb()
        )
    else:
        await message.answer(
            convert_plan_to_message(plan),
            reply_markup=main_kb(User(message)),
            parse_mode=ParseMode.HTML
        )


def convert_plan_to_message(plan: DailyPlan) -> str:
    date_of_plan = plan.date
    if date_of_plan is None:
        raise

    if date_of_plan == dt.date.today():
        date_str = 'сегодня'
    elif date_of_plan == dt.date.today() + dt.timedelta(days=1):
        date_str = 'завтра'
    else:
        date_str = f'{date_of_plan.day}.{date_of_plan.month}.{date_of_plan.year}'

    return "".join([
        b(f'🏆 Топ-3 задачи на {date_str}'),
        "\n\n",
        plan.plan
    ])
