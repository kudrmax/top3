import dataclasses

from aiogram.types import Message


class User:
    tg_id: int

    def __init__(self, data: Message | int | None = None):
        if not data:
            pass
        elif isinstance(data, Message):
            message = data
            self.tg_id = message.from_user.id
        elif isinstance(data, int):
            tg_id = data
            self.tg_id = tg_id

    def set_tg_id(self, tg_id: int):
        self.tg_id = tg_id
        return self

    def to_dict(self):
        return {'tag_id': self.tg_id}
