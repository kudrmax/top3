from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
import datetime as dt

from src.bot.handlers.sevices.create import CreateDailyPlanStateService, PropertyName
from src.bot.keyboards import none, main_kb, today_or_tomorrow_kb, get_plan_kb
from src.bot.states import CreateState
from src.errors import NotAllPlansIsClosed
from src.services.plans.errors import NeedPlanErr, NeedCountErr, NeedDateErr, ThereIsOpenPlanErr
from src.services.plans.service import daily_plans_service

router = Router()


async def try_create_daily_plan(message: Message, state: FSMContext):
    daily_plan = await CreateDailyPlanStateService.get_daily_plan_from_state(state)
    try:
        daily_plans_service.create(daily_plan)
    except NeedPlanErr:
        await get_plan(message, state)
    except NeedCountErr:
        await get_count(message, state)
    except NeedDateErr:
        await get_date(message, state)
    except ThereIsOpenPlanErr:
        pass
    except NotAllPlansIsClosed:
        await message.answer(
            'У вас есть незакрытые планы. Сначала закройте их',
            reply_markup=get_plan_kb()
        )
        await state.clear()
    else:
        await message.answer(
            'Топ-3 задачи добавлены', # TODO иногда на завтра, иногда на сегодня. Нужно указать дату
            reply_markup=get_plan_kb()
        )
        await state.clear()


async def get_plan(message: Message, state: FSMContext):
    await message.answer(
        'Введите топ-3 самые важные задачи в порядке важности',
        reply_markup=none()
    )
    await state.set_state(CreateState.waiting_for_plan)


@router.message(CreateState.waiting_for_plan)
async def set_plan(message: Message, state: FSMContext):
    await CreateDailyPlanStateService.add_data_to_state(state, message.text, PropertyName.PLAN)
    await try_create_daily_plan(message, state)


async def get_count(message: Message, state: FSMContext):
    await message.answer(
        'Введите количество задач',
        reply_markup=none()
    )
    await state.set_state(CreateState.waiting_for_count)


@router.message(CreateState.waiting_for_count)
async def set_count(message: Message, state: FSMContext):
    count = await validate_count(message, message.text)
    if not count:
        return
    await CreateDailyPlanStateService.add_data_to_state(state, count, PropertyName.COUNT)
    await try_create_daily_plan(message, state)


async def get_date(message: Message, state: FSMContext):
    if daily_plans_service.is_date_for_creation_tomorrow():
        date = dt.date.today() + dt.timedelta(days=1)
        await CreateDailyPlanStateService.add_data_to_state(state, date, PropertyName.DATE)
        await try_create_daily_plan(message, state)
    else:
        await message.answer(
            'Вы составляете план на сегодня или на завтра?',
            reply_markup=today_or_tomorrow_kb()
        )
        await state.set_state(CreateState.waiting_for_date)


@router.message(CreateState.waiting_for_date)
async def set_date(message: Message, state: FSMContext):
    date = dt.date.today() + dt.timedelta(days=1) if 'завтра' in message.text else dt.date.today()
    await CreateDailyPlanStateService.add_data_to_state(state, date, PropertyName.DATE)
    await try_create_daily_plan(message, state)


async def validate_count(message: Message, text: str) -> int | None:
    try:
        count = int(text)
    except ValueError:
        await message.answer(
            'Количество задач – это число, поэтому введите число',
            reply_markup=none()
        )
        return None

    if count < 1:
        await message.answer(
            'Количество задач не может быть меньше 1',
            reply_markup=none()
        )
        return None

    return count
