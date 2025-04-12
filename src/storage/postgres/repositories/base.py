import logging
from typing import Dict, Any

from sqlalchemy import Engine, Result, TextClause, text

from src.common.equalablebyattributes import EqualableByAttributes


class Params(EqualableByAttributes):
    params: Dict[str, Any]

    def __init__(self, allow_none: bool = False, **kwargs):
        if allow_none:
            self.params = {k: v for k, v in kwargs.items()}
        else:
            self.params = {k: v for k, v in kwargs.items() if v is not None}

    def to_dict(self):
        return self.params


class BaseRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.logger = logging.getLogger(self.__class__.__name__)

    def execute(self, query: TextClause, params: Params | dict | None = None):
        with self.engine.connect() as conn:
            try:
                if params is not None:
                    result = conn.execute(query, self._get_dict_params(params))
                else:
                    result = conn.execute(query)
                conn.commit()
                return result
            except Exception as e:
                conn.rollback()
                raise e

    @staticmethod
    def _get_dict_params(params: Params | dict):
        if isinstance(params, dict):
            return params
        return params.to_dict()
