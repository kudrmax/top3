import logging
from typing import List
import datetime as dt

from sqlalchemy import Engine, text
from sqlalchemy.exc import IntegrityError

from src.models.daily_plan import DailyPlan, DailyPlanCreate
from src.errors import AlreadyExistsErr, NotAllPlansIsClosed
from src.models.user import User


class DailyPlansRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def create(self, user: User, plan: DailyPlanCreate) -> None:
        if self.get_current(user) is not None:
            raise NotAllPlansIsClosed
        try:
            with self.engine.connect() as conn:
                query = text('''
                    INSERT INTO daily_plans (tg_id, date, plans, count)
                    VALUES (:tg_id, :date, :plans, :count)
                ''')
                params = {
                    "tg_id": plan.tg_id,
                    "date": plan.date,
                    "plans": plan.plan,
                    "count": plan.count,
                }
                conn.execute(query, params)
                conn.commit()
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint' in str(e):
                raise AlreadyExistsErr

    def complete_current(self, user: User, real_complete_count):
        current_goals = self.get_current(user)
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

    def get_current(self, user: User) -> DailyPlan | None:
        with self.engine.connect() as conn:
            query = text('''
                SELECT * FROM daily_plans
                WHERE tg_id = :tg_id
                    AND real_count IS NULL
            ''')
            params = {'tg_id': user.tg_id}
            result = conn.execute(query, params)
            row = result.fetchone()
        if row is None:
            return None
        return self.__convert_row_to_model(row)

    def get_last_closed(self, user: User):
        with self.engine.connect() as conn:
            query = text('''
                SELECT * FROM daily_plans
                WHERE tg_id = :tg_id
                    AND real_count IS NOT NULL
                ORDER BY date DESC
                LIMIT 1
           ''')
            params = {'tg_id': user.tg_id}
            result = conn.execute(query, params)
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
