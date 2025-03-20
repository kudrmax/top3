import dataclasses
import datetime as dt
from typing import List

from src.errors import BadRequestErr


@dataclasses.dataclass
class DailyPlan:
    id: int
    date: dt.date
    plan: str
    count: int
    real_count: int | None = None

    def get_percentage(self) -> int:
        return 100 * self.real_count // self.count


@dataclasses.dataclass
class DailyPlanCreate:
    plan: str | None = None
    count: int | None = None
    date: dt.date | None = None


@dataclasses.dataclass
class DailyPlanStats:
    plans: List[DailyPlan]

    def get_avg_percentage(self, days: int | None = None) -> int:
        if days is None:
            plans = self.plans
        else:
            plans = sorted(self.plans, key=lambda x: x.date)[:days]
        total_count = 0
        total_real_count = 0
        for plan in plans:
            total_count += plan.count
            total_real_count += plan.real_count
        return 100 * total_real_count // total_count
