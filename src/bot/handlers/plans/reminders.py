import datetime as dt
from typing import List

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup

from src.bot.keyboards import reminders_settings_kb, none
from src.bot.states import ReminderSetup
from src.models.user import User
from src.services.reminders.reminder_settings_service import reminder_settings_service

router = Router()


class BadHourErr(Exception):
    pass


class BadMinuteErr(Exception):
    pass


async def setup_reminders(message: Message, state: FSMContext):
    """
    - показать текущие настройки
    - хотите изменить настройки?
        - Когда вам напомнить, что нужно создать задачи.
            - Кнопка: скип
            - Кнопка: отключить напоминание о создании
        - Когда напоминать о задачах?
            - Кнопка: скип
            - Кнопка: отключить напоминание о создании
    """
    reminder_settings = reminder_settings_service.get(User(message))
    if not reminder_settings:
        reminder_settings_str = "У вас пока отключены уведомления"
    else:
        reminder_settings_str = reminder_settings.to_readable_str()

    await message.answer(
        reminder_settings_str,
        reply_markup=reminders_settings_kb()
    )
    await message.answer(
        "Выберите как вы хотите настроить уведомления",
        reply_markup=reminders_settings_kb()
    )


@router.message(StateFilter(None), F.text.lower().contains('по умолчанию'))
async def set_default(message: Message, state: FSMContext):
    pass  # отправить что все ок


@router.message(StateFilter(None), F.text.lower().contains('индивидуально'))
async def set_specific(message: Message, state: FSMContext):
    await message.answer(
        "Когда вы хотите, чтобы вам приходили уведомления о том, что вы не создали задачи?"
        "\n\n"
        "P. S. Если на момент этого времени вы уже создали задачи, то уведомление не придет.",
        reply_markup=none()
    )
    await message.answer(
        'Вводите время в формате "ЧЧ:ММ". Например 10:00 или 07:00".',
        reply_markup=none()
    )
    await state.set_state(ReminderSetup.waiting_for_creation_time)


@router.message(ReminderSetup.waiting_for_creation_time)
async def waiting_for_creation_time(message: Message, state: FSMContext):
    time= await answer_if_bad_time_validation_and_return(message, message.text)
    if not time:
        return
    await state.update_data(creating_time=time)

    await message.answer(
        "Когда вы хотите, чтобы вам приходили уведомления об уже созданных задачах?"
        "\n\n"
        "P. S. Если на момент этого времени у вас нет созданных задач, то уведомления не придут.",
        reply_markup=none()
    )
    await message.answer(
        'Вводите время в следующем формате (каждое время с новой строки):\n'
        'ЧЧ:ММ\nЧЧ:ММ\n\n'
        'Например:\n'
        '12:00\n15:00\n18:00',
        reply_markup=none()
    )

    await state.set_state(ReminderSetup.waiting_for_plan_times)


@router.message(ReminderSetup.waiting_for_plan_times)
async def waiting_for_plan_times(message: Message, state: FSMContext):
    plans_times: List[dt.time] = await answer_if_bad_times_validation_and_return(message)

    data = await state.get_data()
    creating_time = data.get('creating_time')

    add_times_to_reminder_settings(creating_time=creating_time, plans_times=plans_times)


async def answer_if_bad_time_validation_and_return(message: Message, text: str) -> dt.time | None:
    try:
        time = validate_and_return_time(text)
        return time
    except BadHourErr:
        await message.answer(f'Вы ввели "{text}". Час должен быть в пределах от 0 до 23. Введите еще раз.')
    except BadMinuteErr:
        await message.answer(f'Вы ввели "{text}". Минуты должны быть в пределах от 0 до 59. Введите еще раз.')
    except Exception as e:
        await message.answer(
            f'Вы ввели "{text}". Это не соответствует формату "ЧЧ:ММ", например, 10:00 или 07:00. Попробуйте еще раз.')


def validate_and_return_time(text: str) -> dt.time:
    try:
        h, m = text.split(":")
        h, m = int(h), int(m)
        if not 0 <= h <= 23:
            raise BadHourErr
        if not 0 <= m <= 59:
            raise BadMinuteErr
        return dt.time(h, m)
    except Exception as e:
        raise e


async def answer_if_bad_times_validation_and_return(message: Message) -> List[dt.time] | None:
    text = message.text

    times: List[dt.time] = []
    times_str = text.split('\n')
    for time_str in times_str:
        time = await answer_if_bad_time_validation_and_return(message, time_str)
        if not time:
            return
        times.append(time)

    return times


def add_times_to_reminder_settings(creating_time: dt.time, plans_times: List[dt.time]) -> None:
    pass
