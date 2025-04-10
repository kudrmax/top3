import dataclasses
import datetime as dt


@dataclasses.dataclass
class DailyPlan:
    id: int
    tg_id: int
    date: dt.date
    plan: str
    count: int
    real_count: int | None = None


@dataclasses.dataclass
class DailyPlanCreate:
    plan: str | None = None
    count: int | None = None
    date: dt.date | None = None


@dataclasses.dataclass
class DailyPlanUpdate:
    plan: str | None = None
    count: int | None = None
