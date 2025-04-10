from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import datetime as dt

from src.bot.functions.plans.get_current_plan_text import get_current_plan_text
from src.bot.functions.plans.validate_count import validate_count
from src.bot.functions.style import b
from src.bot.handlers.texsts import Texts
from src.bot.sevices.create_plan import CreateDailyPlanStateService, PropertyName
from src.bot.keyboards import none, today_or_tomorrow_kb, get_plan_kb, main_kb
from src.bot.states import CreateState
from src.common.date_and_time import get_today, get_tomorrow
from src.models.user import User
from src.services.plans.errors import NeedPlanErr, NeedCountErr, NeedDateErr
from src.services.plans.service import daily_plans_service

router = Router()

not_all_is_closed_reply = "Вы уже выбрали задачи и пока не закрыли их, поэтому создать задачи не получиться. Сначала закройте эти задачи:"


async def try_create_daily_plan(message: Message, state: FSMContext):
    user = User(message)

    stop = await stop_if_cannot_create_and_reply(message, state)
    if stop:
        return

    daily_plan = await CreateDailyPlanStateService.get_daily_plan_from_state(user, state)
    try:
        daily_plans_service.create(user, daily_plan)
    except NeedPlanErr:
        await get_plan(message, state)
    except NeedCountErr:
        await get_count(message, state)
    except NeedDateErr:
        await get_date(message, state)
    else:
        plan_text = get_current_plan_text(user)
        await message.answer(
            Texts.plan_was_created,
        )
        await message.answer(
            plan_text,
            reply_markup=get_plan_kb(),
            parse_mode=ParseMode.HTML
        )
        await state.clear()


async def get_plan(message: Message, state: FSMContext):
    await message.answer(
        Texts.need_plan,
        reply_markup=none(),
        parse_mode=ParseMode.HTML
    )
    is_tomorrow = daily_plans_service.is_date_for_creation_tomorrow(User(message))
    if is_tomorrow:
        await message.answer(
            f"Обращаю внимание, что вы создаете задачи на {b('завтра')}, так как сегодня вы уже выполнили свои задачи!",
            reply_markup=none(),
            parse_mode=ParseMode.HTML
        )
    await state.set_state(CreateState.waiting_for_plan)


@router.message(CreateState.waiting_for_plan)
async def set_plan(message: Message, state: FSMContext):
    await CreateDailyPlanStateService.add_data_to_state(User(message), state, message.text, PropertyName.PLAN)
    await try_create_daily_plan(message, state)


async def get_count(message: Message, state: FSMContext):
    await message.answer(
        'Сколько задач вы ввели?',
        reply_markup=none()
    )
    await state.set_state(CreateState.waiting_for_count)


@router.message(CreateState.waiting_for_count)
async def set_count(message: Message, state: FSMContext):
    count_text = message.text
    count = await validate_count(message, count_text)
    if not count:
        return
    await CreateDailyPlanStateService.add_data_to_state(User(message), state, count, PropertyName.COUNT)
    await try_create_daily_plan(message, state)


async def get_date(message: Message, state: FSMContext):
    if daily_plans_service.is_date_for_creation_tomorrow(User(message)):
        date = get_today() + dt.timedelta(days=1)
        await CreateDailyPlanStateService.add_data_to_state(User(message), state, date, PropertyName.DATE)
        await try_create_daily_plan(message, state)
    else:
        await message.answer(
            'Вы составляете план на сегодня или на завтра?',
            reply_markup=today_or_tomorrow_kb()
        )
        await state.set_state(CreateState.waiting_for_date)


@router.message(CreateState.waiting_for_date)
async def set_date(message: Message, state: FSMContext):
    date = get_today() + dt.timedelta(days=1) if 'завтра' in message.text else dt.date.today()
    await CreateDailyPlanStateService.add_data_to_state(User(message), state, date, PropertyName.DATE)
    await try_create_daily_plan(message, state)


async def get_not_all_is_closed_reply(message: Message, state: FSMContext):
    await message.answer(
        not_all_is_closed_reply
    )
    await message.answer(
        get_current_plan_text(User(message)),
        reply_markup=get_plan_kb(),
        parse_mode=ParseMode.HTML
    )
    await state.clear()


async def stop_if_cannot_create_and_reply(message: Message, state: FSMContext) -> bool:
    user = User(message)
    if daily_plans_service.not_all_is_closed(user):
        await get_not_all_is_closed_reply(message, state)
        return True

    last_closed_plan_date = daily_plans_service.get_last_closed_plan_date(user)
    if last_closed_plan_date == get_tomorrow():
        await message.answer(
            "Вы уже закрыли задачи и на сегодня, и на завтра. Дождитесь следующего дня, чтобы создать новые.",
            reply_markup=main_kb(user)
        )
        return True

    return False
