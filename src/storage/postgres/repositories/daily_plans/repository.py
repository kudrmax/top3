from datetime import datetime
from typing import List

from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from src.models.daily_plan import DailyPlan, DailyPlanCreate, DailyPlanUpdate
from src.errors.base_errors import NotFoundErr
from src.models.user import User
from src.storage.postgres.connection import engine
from src.storage.postgres.repositories.base import BaseRepository, Params
from src.storage.postgres.repositories.daily_plans.errors import PlanAlreadyExistsWithThisDateErr, OpenPlanNotFoundErr


class DailyPlansRepository(BaseRepository):
    def create(self, user: User, plan: DailyPlanCreate) -> None:
        try:
            query = text('''
                INSERT INTO daily_plans (tg_id, date, plans, count)
                VALUES (:tg_id, :date, :plans, :count)
            ''')
            params = Params(
                tg_id=user.tg_id,
                date=plan.date,
                plans=plan.plan,
                count=plan.count,
            )
            self.execute(query, params)
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint' in str(e):
                raise PlanAlreadyExistsWithThisDateErr(user=user.to_dict(), date=plan.date)

    def update(self, user: User, plan_id: int, plan_update: DailyPlanUpdate) -> None:
        current_plan = self.get_open_plan(user)
        if current_plan is None:
            raise NotFoundErr

    def get_open_plan(self, user: User) -> DailyPlan | None:
        query = text('''
            SELECT * FROM daily_plans
            WHERE tg_id = :tg_id
                AND real_count IS NULL
        ''')
        params = Params(tg_id=user.tg_id)
        result = self.execute(query, params)
        row = result.fetchone()
        return self.__convert_row_to_model(row)

    def complete_open_plan(self, user: User, real_complete_count: int) -> None:
        current_plan = self.get_open_plan(user)
        if current_plan is None:
            raise OpenPlanNotFoundErr(user=user.to_dict())

        query = text('''
            UPDATE daily_plans
            SET real_count = :real_count
            WHERE id = :id;
        ''')
        params = Params(
            id=current_plan.id,
            real_count=real_complete_count,
        )
        self.execute(query, params)

    def get_last_closed_plan_by_user(self, user: User) -> DailyPlan | None:
        query = text('''
            SELECT * FROM daily_plans
            WHERE tg_id = :tg_id
                AND real_count IS NOT NULL
            ORDER BY date DESC
            LIMIT 1
       ''')
        params = Params(tg_id=user.tg_id)
        result = self.execute(query, params)
        row = result.fetchone()
        return self.__convert_row_to_model(row)

    def get_by_id(self, user: User, id: int) -> DailyPlan | None:
        query = text('''
            SELECT * FROM daily_plans
            WHERE id = :id
            LIMIT 1
        ''')
        params = Params(id=id)
        result = self.execute(query, params)
        row = result.fetchone()
        return self.__convert_row_to_model(row)

    @staticmethod
    def __convert_row_to_model(row) -> DailyPlan | None:
        if row is None:
            return None
        return DailyPlan(*row)

    def __convert_rows_to_models(self, rows) -> List[DailyPlan]:
        plans = []
        for row in rows:
            plan = self.__convert_row_to_model(row)
            if plan:
                plans.append(plan)
        return plans
