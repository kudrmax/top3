from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.functions.plans.get_current_plan_text import get_current_plan_text
from src.bot.functions.style import b
from src.bot.handlers.texsts import Texts
from src.bot.keyboards import none, create_plan_kb, get_plan_kb, main_kb
from src.bot.states import CompleteState
from src.common.date_and_time import get_tomorrow
from src.models.user import User
from src.services.plans.service import daily_plans_service

router = Router()


async def complete_plan(message: Message, state: FSMContext):
    if daily_plans_service.all_is_closed(User(message)):
        await message.answer(
            "Вы еще не создали задачи. Сначала создайте их",
            reply_markup=create_plan_kb()
        )
        return

    current = daily_plans_service.get_current(User(message))
    if current.date == get_tomorrow():
        await message.answer(
            f'У вас есть созданные задачи, но они созданы на {b("завтра")}. Дождитесь завтра, чтобы закрыть их.',
            parse_mode=ParseMode.HTML
        )
        await message.answer(
            get_current_plan_text(User(message)),
            reply_markup=get_plan_kb(),
            parse_mode=ParseMode.HTML
        )
        return

    await message.answer(
        "Сколько задач вы выполнили?",
        reply_markup=none()
    )
    await message.answer(
        get_current_plan_text(User(message)),
        reply_markup=none(),
        parse_mode=ParseMode.HTML
    )
    await state.set_state(CompleteState.waiting_for_number)


@router.message(CompleteState.waiting_for_number)
async def complete(message: Message, state: FSMContext):
    real_complete_count = await validate_real_count(message)
    if real_complete_count is None:
        return

    daily_plans_service.complete_current(User(message), real_complete_count)
    last_plan = daily_plans_service.get_last_closed_plan_by_user(User(message))
    real = last_plan.real_count
    expected = last_plan.count

    await message.answer(
        f"🎉 Задачи на сегодня закрыты.\n\n"
        f"Вы выполнили {real} из {expected} задач!\n\n"
        f"Теперь вы можете поставить новые задачи.",
        reply_markup=create_plan_kb()
    )
    await state.clear()


async def validate_real_count(message: Message) -> int | None:
    try:
        real_complete_count = int(message.text)
    except ValueError:
        await message.answer(
            'Количество задач – это число, поэтому введите число.',
            reply_markup=none()
        )
        return

    if real_complete_count < 0:
        await message.answer(
            'Количество задач не может быть меньше 0.',
            reply_markup=none()
        )
        return

    plan = daily_plans_service.get_current(User(message))
    if real_complete_count > plan.count:
        await message.answer(
            'Вы не могли закрыть больше задач, чем запланировали.'
            f'Введите число меньшее или равное {plan.count}.',
            reply_markup=none()
        )
        return

    return real_complete_count
