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
    if daily_plans_service.all_is_closed(user):
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
        ['Посмотреть задачи', 'Изменить задачи'],
        ['Подтвердить выполнение задач'],
        ['Настроить уведомления'],
        ['Сообщить о баге'],
    ])


def reminders_settings_kb():
    return make_keyboard_by_lists([
        ['Выбрать время по умолчанию'],
        ['Настроить индивидуально'],
    ])


def reminders_settings_concrete_kb():
    return make_keyboard_by_lists([
        ['Выбрать время по умолчанию'],
        ['Не менять эту настройку'],
    ])
