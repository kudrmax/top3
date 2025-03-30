from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from src.models.user import User
from src.services.plans.service import daily_plans_service


def make_keyboard_by_lists(items: list[list[str]]) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=item) for item in row]
        for row in items
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def none():
    return ReplyKeyboardRemove()


def main_kb(user: User):
    if daily_plans_service.is_all_closed(user):
        return create_plan_kb()
    return get_plan_kb()


def today_or_tomorrow_kb():
    return make_keyboard_by_lists([
        ['На сегодня', 'На завтра']
    ])


def create_plan_kb():
    return make_keyboard_by_lists([
        ['Создать задачи']
    ])


def get_plan_kb():
    return make_keyboard_by_lists([
        ['Посмотреть задачи'],
        ['Подтвердить выполнение задач'],
        ['🚧 Изменить задачи'],
        ['Сообщить о баге'],
    ])
