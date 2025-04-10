from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup

from src.bot.functions.plans.get_current_plan_text import get_current_plan_text
from src.bot.functions.plans.validate_count import validate_count
from src.bot.keyboards import none, create_plan_kb, main_kb, get_plan_kb
from src.bot.states import UpdateState
from src.models.daily_plan import DailyPlanUpdate
from src.models.user import User
from src.services.plans.errors import ThereIsNoOpenPlanErr
from src.services.plans.service import daily_plans_service

router = Router()


async def update_plan(message: Message, state: FSMContext):
    """
    # отобразить план
    # спросить что хочу изменить
        # изменить планы
            # попросить ввести новые планы
            # Спросить сколько тепепрь задач
            # ок
        # изменить дату
            # если date == сегодня
                # вы хотите изменить планы с сегодня на завтра?
                # МОЖНО МЕНЯТЬ
            # если date == завтра
                # если последний закрытый план сегодня
                    # НЕЛЬЗЯ МЕНЯТЬ
                # если последний закрытый план не сегодня
                    # вы хотите изменить планы с завтра на сегодня?
                    # МОЖНО МЕНЯТЬ
    """
    await message.answer(
        get_current_plan_text(User(message)),
        reply_markup=none(),
        parse_mode=ParseMode.HTML,
    )

    await message.answer(
        "Введите новый текст плана.\n\n",
        reply_markup=none(),
        parse_mode=ParseMode.HTML,
    )

    await state.set_state(UpdateState.waiting_for_text)


@router.message(UpdateState.waiting_for_text)
async def update_text(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(text=text)

    await message.answer(
        "Сколько задач вы ввели?",
        reply_markup=none(),
        parse_mode=ParseMode.HTML,
    )
    await state.set_state(UpdateState.waiting_for_number)


@router.message(UpdateState.waiting_for_number)
async def update_text(message: Message, state: FSMContext):
    count_text = message.text
    count = await validate_count(message, count_text)
    if not count:
        return
    text = (await state.get_data()).get('text')
    try:
        daily_plans_service.update_current(
            user=User(message),
            plan_data=DailyPlanUpdate(
                plan=text,
                count=count,
            )
        )
        await message.answer(
            "Задачи успешно обновлены. Новые задачи:",
            reply_markup=get_plan_kb(),
            parse_mode=ParseMode.HTML,
        )
        await message.answer(
            get_current_plan_text(User(message)),
            parse_mode=ParseMode.HTML,
        )
    except ThereIsNoOpenPlanErr:
        await message.answer(
            "У вас нет созданных задач. Сначала создайте их",
            reply_markup=create_plan_kb(),
            parse_mode=ParseMode.HTML,
        )
    await state.clear()
