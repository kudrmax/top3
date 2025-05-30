import datetime as dt

from src.errors.base_errors import AlreadyExistsErr, NotFoundErr


class PlanAlreadyExistsWithThisDateErr(AlreadyExistsErr):
    message = f"There is already a plan for this date and this user"

    def __init__(self, user: dict, date: dt.date, datetime: dt.datetime | None = None):
        self.details = {
            'user': user,
            'date': date
        }
        if datetime:
            self.details['datetime'] = datetime


class OpenPlanNotFoundErr(NotFoundErr):
    message = f"Open plans not found for this user"

    def __init__(self, user: dict):
        self.details = {'user': user}
