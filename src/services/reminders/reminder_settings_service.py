import logging
from typing import List

from src.models.reminders.reminder_settings import ReminderSettingUpsert, ReminderSetting
from src.models.user import User
from src.storage.postgres.connection import engine
from src.storage.postgres.repositories.reminder_serttings.repository import ReminderSettingRepository


class ReminderSettingsService:
    def __init__(self, reminder_repository: ReminderSettingRepository):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.reminder_repository = reminder_repository

    def get_all(self) -> List[ReminderSetting]:
        return self.reminder_repository.get_all()

    def get(self, user: User) -> ReminderSetting | None:
        return self.reminder_repository.get(user)

    def upsert(self, user: User, reminder_setting: ReminderSettingUpsert) -> None:
        return self.reminder_repository.upsert(user, reminder_setting)


reminder_settings_service = ReminderSettingsService(
    reminder_repository=ReminderSettingRepository(
        engine=engine,
    )
)
