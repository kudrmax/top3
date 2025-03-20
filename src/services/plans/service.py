import logging
import datetime as dt

from src.models.daily_plan import DailyPlanCreate, DailyPlan
from src.services.plans.errors import NeedPlanErr, NeedCountErr, NeedDateErr, ThereIsOpenPlanErr
from src.storage.postgres.connection import engine
from src.storage.postgres.repositories.daily_goals import DailyGoalsRepository


class DailyGoalsService:
    def __init__(self, repository: DailyGoalsRepository):
        self.repository = repository
        self.logger = logging.getLogger(self.__class__.__name__)

    def create(self, plan_create: DailyPlanCreate) -> None:
        self._raise_if_not_ready_for_create(plan_create)
        self.repository.create(plan_create)

    def get_current(self) -> DailyPlan | None:
        return self.repository.get_current()

    def complete_current(self, real_complete_count):
        return self.repository.complete_current(real_complete_count)

    def is_all_closed(self) -> bool:
        return self.get_current() is None

    def is_date_for_creation_tomorrow(self):
        current_date = dt.date.today()
        last_plan = self.repository.get_last_closed()
        if last_plan is None:
            return False
        last_plan_create_date = last_plan.date
        if current_date == last_plan_create_date:
            return True
        return False


    def _raise_if_not_ready_for_create(self, plan_create: DailyPlanCreate):
        if not plan_create.plan:
            raise NeedPlanErr
        if not plan_create.count:
            raise NeedCountErr
        if not plan_create.date:
            raise NeedDateErr
        if not self.is_all_closed():
            raise ThereIsOpenPlanErr

    def get_stat(self):
        pass

daily_plans_service = DailyGoalsService(DailyGoalsRepository(engine=engine))
