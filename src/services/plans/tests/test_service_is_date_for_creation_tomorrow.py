import dataclasses
import datetime as dt

import pytest

from src.common.date_and_time import get_today
from src.common.testcase import TestCaseBase
from src.models.daily_plan import DailyPlan
from src.models.user import User


@dataclasses.dataclass(frozen=True)
class TestCase(TestCaseBase):
    user: User
    last_plan: DailyPlan | None
    expected_result: bool


today = get_today()
yesterday = today - dt.timedelta(days=1)
tomorrow = today + dt.timedelta(days=1)


@pytest.mark.parametrize(
    "test_case",
    [
        TestCase(
            user=User(666),
            last_plan=DailyPlan(
                date=today,
                id=1,
                tg_id=666,
                plan="some plan",
                count=3,
                real_count=2,
            ),
            expected_result=True,
        ),
        TestCase(
            user=User(666),
            last_plan=DailyPlan(
                date=yesterday,
                id=1,
                tg_id=666,
                plan="some plan",
                count=3,
                real_count=2,
            ),
            expected_result=False,
        ),
        TestCase(
            user=User(666),
            last_plan=DailyPlan(
                date=tomorrow,
                id=1,
                tg_id=666,
                plan="some plan",
                count=3,
                real_count=2,
            ),
            expected_result=False,  # такая ситуация не имеет смысла и невозможна, но формально ответ False
        ),
        TestCase(
            user=User(666),
            last_plan=None,
            expected_result=False,
        ),
    ]
)
def test_service_is_date_for_creation_tomorrow(mock_service, test_case):
    user, last_plan, expected_result = test_case.get_data()

    mock_service.repository.get_last_closed_plan_by_user.return_value = last_plan

    result = mock_service.is_date_for_creation_tomorrow(user)
    assert result == expected_result
