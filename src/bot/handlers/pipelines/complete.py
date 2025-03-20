from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.keyboards import none, create_plan_kb
from src.bot.states import CompleteState
from src.services.plans.service import daily_plans_service

router = Router()


async def complete_plan(message: Message, state: FSMContext):
    if daily_plans_service.get_current() is None:
        await message.answer(
            "У вас нет открытых задач. Сначала создайте задачи.",
            reply_markup=create_plan_kb()
        )
    else:
        # TODO добавить проверку на то, если на задаче дата завтра, а мы сегодня, то нельзя закрыть задачи (до наступления дня)
        await message.answer(
            "Сколько задач вы закрыли?",
            reply_markup=none()
        )
        await state.set_state(CompleteState.waiting_for_number)


@router.message(CompleteState.waiting_for_number)
async def complete(message: Message, state: FSMContext):
    real_complete_count = int(message.text)
    daily_plans_service.complete_current(real_complete_count)
    await message.answer(
        "Задачи на сегодня закрыты. Вы можете поставить новые задачи.",
        reply_markup=create_plan_kb()
    )
    await state.clear()
