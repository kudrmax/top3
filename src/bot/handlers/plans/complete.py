from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.handlers.texsts import Texts
from src.bot.keyboards import none, create_plan_kb
from src.bot.states import CompleteState
from src.models.user import User
from src.services.plans.service import daily_plans_service

router = Router()


async def complete_plan(message: Message, state: FSMContext):
    if daily_plans_service.get_current(User(message)) is None:
        await message.answer(
            Texts.plan_is_not_created,
            reply_markup=create_plan_kb()
        )
    else:
        # TODO добавить проверку на то, если на задаче дата завтра, а мы сегодня, то нельзя закрыть задачи (до наступления дня)
        await message.answer(
            "Сколько задач вы выполнили?",
            reply_markup=none()
        )
        await state.set_state(CompleteState.waiting_for_number)


@router.message(CompleteState.waiting_for_number)
async def complete(message: Message, state: FSMContext):
    real_complete_count = await validate_real_count(message)
    if real_complete_count is None:
        return
    daily_plans_service.complete_current(User(message), real_complete_count)

    await message.answer(
        "Задачи на сегодня закрыты. Теперь вы можете поставить новые задачи.",
        reply_markup=create_plan_kb()
    )
    await state.clear()


async def validate_real_count(message: Message) -> int | None:
    try:
        real_complete_count = int(message.text)
    except ValueError:
        await message.answer(
            'Количество задач – это число, поэтому введите число',
            reply_markup=none()
        )
        return

    if real_complete_count < 0:
        await message.answer(
            'Количество задач не может быть меньше 0',
            reply_markup=none()
        )
        return

    plan = daily_plans_service.get_current(User(message))
    if real_complete_count > plan.count:
        await message.answer(
            'Вы не могли закрыть больше задач, чем запланировали.'
            f'Введите число меньшее или равное {plan.count}',
            reply_markup=none()
        )
        return

    return real_complete_count
