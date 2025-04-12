from src.errors.base_exception import MyException


class CannotParseTime(MyException):
    def __init__(self, date_str: str):
        self.details = {
            'date_str': date_str,
        }
