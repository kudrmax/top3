from typing import List

from sqlalchemy import text

from src.models.reminders.reminder_settings import ReminderSettingUpsert, ReminderSetting
from src.models.user import User
from src.storage.postgres.repositories.base import BaseRepository, Params


class ReminderSettingRepository(BaseRepository):
    def upsert(self, user: User, reminder_setting: ReminderSettingUpsert) -> None:
        query = text('''
            INSERT INTO reminder_settings (tg_id, creation_reminder_time, reminder_times)
            VALUES (:tg_id, :creation_reminder_time, :reminder_times)
            ON CONFLICT (tg_id) DO UPDATE SET
                creation_reminder_time = EXCLUDED.creation_reminder_time,
                reminder_times = EXCLUDED.reminder_times
        ''')
        params = Params(
            allow_none=True,
            tg_id=user.tg_id,
            creation_reminder_time=reminder_setting.get_creation_reminder_time_str(),
            reminder_times=reminder_setting.get_reminder_times_str_list(),
        )
        self.execute(query, params)

    def get(self, user: User) -> ReminderSetting | None:
        query = text('''
            SELECT tg_id, creation_reminder_time, reminder_times
            FROM reminder_settings
            WHERE tg_id = :tg_id
        ''')
        params = Params(tg_id=user.tg_id)
        result = self.execute(query, params)
        row = result.fetchone()
        return self.__convert_row_to_model(row)

    def get_all(self) -> List[ReminderSetting]:
        query = text('''
            SELECT tg_id, creation_reminder_time, reminder_times
            FROM reminder_settings
        ''')
        result = self.execute(query)
        return self.__convert_rows_to_models(result)

    @staticmethod
    def __convert_row_to_model(row) -> ReminderSetting | None:
        if row is None:
            return None
        return ReminderSetting(*row)

    def __convert_rows_to_models(self, rows) -> List[ReminderSetting]:
        plans = []
        for row in rows:
            plan = self.__convert_row_to_model(row)
            if plan:
                plans.append(plan)
        return plans
