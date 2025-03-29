import logging
from typing import Dict, Any

from sqlalchemy import Engine, Result, TextClause, text

from src.common.equalablebyattributes import EqualableByAttributes


class Params(EqualableByAttributes):
    params: Dict[str, Any]

    def __init__(self, **kwargs):
        self.params = {k: v for k, v in kwargs.items() if v is not None}

    def to_dict(self):
        return self.params


class BaseRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute(self, query: TextClause, params: Params):
        with self.engine.connect() as conn:
            try:
                result = conn.execute(query, params.to_dict())
                conn.commit()
                return result
            except Exception as e:
                conn.rollback()
                raise e