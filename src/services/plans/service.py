import logging
import datetime as dt

from src.common.date_and_time import get_today
from src.models.daily_plan import DailyPlanCreate, DailyPlan
from src.models.user import User
from src.services.plans.errors import NeedPlanErr, NeedCountErr, NeedDateErr, ThereIsOpenPlanErr
from src.storage.postgres.connection import engine
from src.storage.postgres.repositories.daily_plans.repository import DailyPlansRepository
from src.storage.postgres.repositories.daily_plans.errors import PlanAlreadyExistsWithThisDateErr, OpenPlanNotFoundErr


class DailyPlansService:
    def __init__(self, repository: DailyPlansRepository):
        self.repository = repository
        self.logger = logging.getLogger(self.__class__.__name__)

    def create(self, user: User, plan_create: DailyPlanCreate) -> None:
        self._raise_if_not_ready_to_create(plan_create)
        self._raise_if_cannot_create(user)
        self.repository.create(user, plan_create)

    def get_current(self, user: User) -> DailyPlan | None:
        return self.repository.get_open_plan(user)

    def complete_current(self, user: User, real_complete_count: int) -> None:
        return self.repository.complete_open_plan(user, real_complete_count)

    def there_are_not_closed(self, user: User) -> bool:
        return not self.is_all_closed(user)

    def is_all_closed(self, user: User) -> bool:
        return self.get_current(user) is None

    def is_date_for_creation_tomorrow(self, user: User) -> bool:
        last_plan = self.get_last_closed_plan_by_user(user)
        if last_plan is None:
            return False
        current_date = get_today()
        last_plan_create_date = last_plan.date
        if current_date == last_plan_create_date:
            return True
        return False

    def get_last_closed_plan_by_user(self, user: User) -> DailyPlan | None:
        return self.repository.get_last_closed_plan_by_user(user)

    def _raise_if_not_ready_to_create(self, plan_create: DailyPlanCreate):
        if not plan_create.plan:
            raise NeedPlanErr
        if not plan_create.count:
            raise NeedCountErr
        if not plan_create.date:
            raise NeedDateErr

    def _raise_if_cannot_create(self, user: User):
        if self.there_are_not_closed(user):
            raise ThereIsOpenPlanErr


daily_plans_service = DailyPlansService(DailyPlansRepository(engine=engine))
