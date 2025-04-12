import dataclasses
import datetime as dt
from typing import List

from src.models.reminders.errors import CannotParseTime


@dataclasses.dataclass
class ReminderSettingUpsert:
    creation_reminder_time: dt.time | None = None
    reminder_times: List[dt.time] | None = None

    def get_creation_reminder_time_str(self) -> str | None:
        return self._convert_time_to_str(self.creation_reminder_time)

    def get_reminder_times_str_list(self) -> List[str]:
        if self.reminder_times is None:
            return []

        result = []
        for t in self.reminder_times:
            if t is None:
                continue
            result.append(self._convert_time_to_str(t))
        return result

    def _convert_time_to_str(self, t: dt.time) -> str | None:
        if t is None:
            return None
        return t.strftime('%H:%M')


class ReminderSetting:
    tg_id: int
    creation_reminder_time: dt.time | None = None
    reminder_times: List[dt.time]

    def __init__(
            self,
            tg_id: int,
            creation_reminder_time_str: str | None = None,
            reminder_times_str: List[str] | None = None,
    ):
        self.tg_id = tg_id
        self.creation_reminder_time = self._convert_str_to_time(creation_reminder_time_str)
        self.reminder_times = [self._convert_str_to_time(t) for t in reminder_times_str]

    def init_from_upsert_model(self, model: ReminderSettingUpsert):
        self.creation_reminder_time = model.creation_reminder_time
        self.reminder_times = model.reminder_times

    def get_times(self) -> List[dt.time]:
        result = []

        time = self.creation_reminder_time
        if time is not None:
            result.append(time)

        times = self.reminder_times
        if times is not None and len(times) > 0:
            for time in times:
                result.append(time)

        return result

    @staticmethod
    def _convert_str_to_time(time_str: str) -> dt.time | None:
        if time_str is None:
            return None
        try:
            parsed_time = dt.datetime.strptime(time_str, "%H:%M")
            return parsed_time.time()
        except ValueError:
            raise CannotParseTime(date_str=time_str)
