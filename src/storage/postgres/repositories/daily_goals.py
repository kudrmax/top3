import logging
from typing import List
import datetime as dt

from sqlalchemy import Engine, text
from sqlalchemy.exc import IntegrityError

from src.models.daily_plan import DailyPlan, DailyPlanCreate
from src.errors import AlreadyExistsErr, NotAllPlansIsClosed


class DailyGoalsRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def create(self, new_goal: DailyPlanCreate) -> None:
        if self.get_current() is not None:
            raise NotAllPlansIsClosed
        try:
            with self.engine.connect() as conn:
                query = text('''
                    INSERT INTO daily_plans (date, plans, count)
                    VALUES (:date, :plans, :count)
                ''')
                params = {
                    "date": new_goal.date,
                    "plans": new_goal.plan,
                    "count": new_goal.count,
                }
                conn.execute(query, params)
                conn.commit()
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint' in str(e):
                raise AlreadyExistsErr

    def complete_current(self, real_complete_count):
        current_goals = self.get_current()
        if current_goals is None:
            raise

        with self.engine.connect() as conn:
            query = text('''
                UPDATE daily_plans
                SET real_count = :real_count
                WHERE id = :id;
            ''')
            params = {
                "id": current_goals.id,
                "real_count": real_complete_count,
            }
            conn.execute(query, params)
            conn.commit()

    def get_current(self) -> DailyPlan | None:
        with self.engine.connect() as conn:
            query = text('''
                SELECT * FROM daily_plans
                WHERE real_count IS NULL
            ''')
            result = conn.execute(query)
            row = result.fetchone()
        if row is None:
            return None
        return self.__convert_row_to_model(row)

    def get_last_closed(self):
        with self.engine.connect() as conn:
            query = text('''
               SELECT * FROM daily_plans
               WHERE real_count IS NOT NULL
               ORDER BY date DESC
               LIMIT 1
           ''')
            result = conn.execute(query)
            row = result.fetchone()
        if row is None:
            return None
        return self.__convert_row_to_model(row)

    @staticmethod
    def __convert_row_to_model(row) -> DailyPlan:
        return DailyPlan(*row)

    @staticmethod
    def __convert_rows_to_models(rows) -> List[DailyPlan]:
        return [DailyPlan(*row) for row in rows]
