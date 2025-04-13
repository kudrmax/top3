from src.errors.base_exception import MyException


class Err500(MyException):
    def __init__(self, message):
        self.details = {'message': message}


class BadRequestErr(MyException):
    pass


class NotFoundErr(MyException):
    pass


class AlreadyExistsErr(MyException):
    pass
