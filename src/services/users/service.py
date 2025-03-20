from src.models.user import UserCreate
from src.storage.postgres.repositories.users import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def is_user_exists(self, telegram_id: int) -> bool:
        return self.repository.get_by_telegram_id(telegram_id) is not None

    def create(self, user: UserCreate):
        self.repository.create(user)
