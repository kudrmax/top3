import logging
from typing import List

from sqlalchemy import Engine, text
from sqlalchemy.exc import IntegrityError

from src.errors import AlreadyExistsErr
from src.models.user import UserCreate, User


class UserRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def create(self, user: UserCreate):
        try:
            with self.engine.connect() as conn:
                query = text('''
                    INSERT INTO users (telegram_id)
                    VALUES (:telegram_id)
                ''')
                params = {"telegram_id": user.telegram_id}
                conn.execute(query, params)
                conn.commit()
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint' in str(e):
                raise AlreadyExistsErr

    def get_by_telegram_id(self, telegram_id: int):
        with self.engine.connect() as conn:
            query = text('''
                SELECT * FROM users
                WHERE telegram_id = :telegram_id
                LIMIT 1
            ''')
            params = {"telegram_id": telegram_id}
            result = conn.execute(query, params)
            row = result.fetchone()
            if row is None:
                return None
            return self.__convert_row_to_model(row)

    @staticmethod
    def __convert_row_to_model(row) -> User:
        return User(*row)

    @staticmethod
    def __convert_rows_to_models(rows) -> List[User]:
        return [User(*row) for row in rows]
