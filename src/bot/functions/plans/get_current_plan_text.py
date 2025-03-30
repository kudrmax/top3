from src.bot.functions.plans.get_plans_text import get_plan_text
from src.errors.base_exception import MyException
from src.models.daily_plan import DailyPlan
from src.models.user import User
from src.services.plans.service import daily_plans_service


def get_current_plan_text(user: User) -> str | None:
    plan = daily_plans_service.get_current(user)
    if plan is None:
        return None
    return convert_plan_to_message(plan)


def convert_plan_to_message(plan: DailyPlan) -> str:
    date_of_plan = plan.date
    if date_of_plan is None:
        raise MyException("There is no date in the plan", plan=plan)

    return get_plan_text(plan.plan, plan.date)
