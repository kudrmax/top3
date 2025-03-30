from src.errors.base_exception import MyException
from src.models.user import User


class NeedPlanErr(MyException):
    message = "Need a plan"


class NeedCountErr(MyException):
    message = "Need count"


class NeedDateErr(MyException):
    message = "Need date"


class ThereIsOpenPlanErr(MyException):
    message = "There is open plan"
