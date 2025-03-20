import dataclasses


@dataclasses.dataclass
class User:
    id: int
    telegram_id: int


@dataclasses.dataclass
class UserCreate:
    telegram_id: int
