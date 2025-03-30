import datetime as dt

import pytz


def get_today():
    timezone = pytz.timezone('Europe/Moscow')
    now = dt.datetime.now(timezone)
    today = now.date()
    return today


def get_tomorrow():
    today = get_today()
    return today + dt.timedelta(days=1)
