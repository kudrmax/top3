import dataclasses

from aiogram.types import Message


class User:
    tg_id: int

    def __init__(self, message: Message):
        self.tg_id = message.from_user.id
