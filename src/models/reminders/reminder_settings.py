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

    @staticmethod
    def _convert_str_to_time(time_str: str) -> dt.time | None:
        if time_str is None:
            return None
        try:
            parsed_time = dt.datetime.strptime(time_str, "%H:%M")
            return parsed_time.time()
        except ValueError:
            raise CannotParseTime(date_str=time_str)

    def __init__(
            self,
            tg_id: int,
            creation_reminder_time_str: str | None = None,
            reminder_times_str: List[str] | None = None,
    ):
        self.tg_id = tg_id
        self.creation_reminder_time = self._convert_str_to_time(creation_reminder_time_str)
        self.reminder_times = [self._convert_str_to_time(t) for t in reminder_times_str]

    def enrich_from_upsert_model(self, model: ReminderSettingUpsert):
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

    def to_readable_str(self):
        creation_reminder_header = "Время уведомлений о том, что вы еще не создали задачи:"
        plan_reminder_header = "Время уведомлений о самих задачах:"
        not_set_reminder_header = "Не указано"

        creation_reminder_time_list = [
            self.creation_reminder_time] if self.creation_reminder_time else not_set_reminder_header
        plan_reminder_times_list = [
            f'{t.hour:02}:{t.minute:02}' for t in self.reminder_times
        ] if (self.reminder_times or len(self.reminder_times) > 0) else not_set_reminder_header

        if creation_reminder_time_list != not_set_reminder_header:
            creation_reminder_time_str = "\n".join(f'- {t}' for t in creation_reminder_time_list)
        else:
            creation_reminder_time_str = creation_reminder_time_list

        if plan_reminder_times_list != not_set_reminder_header:
            plan_reminder_times_str = "\n".join(f'- {t}' for t in plan_reminder_times_list)
        else:
            plan_reminder_times_str = plan_reminder_times_list

        result_list = [
            creation_reminder_header + '\n',
            creation_reminder_time_str + '\n',
            '\n',
            plan_reminder_header + '\n',
            plan_reminder_times_str + '\n',
        ]

        return "".join(result_list)
