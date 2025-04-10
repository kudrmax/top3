import datetime as dt

import pytz

timezone = pytz.timezone('Europe/Moscow')


def get_now():
    return dt.datetime.now(timezone)


def get_today():
    now = get_now()
    today = now.date()
    return today


def get_tomorrow():
    today = get_today()
    return today + dt.timedelta(days=1)
