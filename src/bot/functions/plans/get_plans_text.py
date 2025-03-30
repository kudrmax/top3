import datetime as dt

from src.bot.functions.style import b
from src.common.date_and_time import get_today, get_tomorrow


def get_header(date: dt.date):
    if date is None:
        return b(f'🏆 Топ-3 задачи')

    if date == get_today():
        date_str = 'сегодня'
    elif date == get_tomorrow():
        date_str = 'завтра'
    else:
        date_str = f'{date.day}.{date.month}.{date.year}'

    return b(f'🏆 Топ-3 задачи на {date_str}')


def get_plan_text(plan: str, date: dt.date | None = None) -> str:
    header = get_header(date)

    return "\n\n".join([
        header,
        plan
    ])
