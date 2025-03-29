from src.errors.base_exception import MyException


class BadRequestErr(MyException):
    pass


class NotFoundErr(MyException):
    pass


class AlreadyExistsErr(MyException):
    pass


