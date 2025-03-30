import dataclasses

import pytest
import datetime as dt

from src.common.testcase import TestCaseBase
from src.models.daily_plan import DailyPlan
from src.models.user import User


@dataclasses.dataclass(frozen=True)
class TestCase(TestCaseBase):
    user: User
    expected_plan: DailyPlan | None


@pytest.mark.parametrize(
    "test_case",
    [
        TestCase(
            user=User(666),
            expected_plan=DailyPlan(
                id=1,
                tg_id=666,
                date=dt.date(2020, 1, 1),
                plan="some plan",
                count=3,
            )
        ),
        TestCase(
            user=User(666),
            expected_plan=None
        ),
    ]
)
def test_service_get_success(mock_service, test_case):
    user, expected_plan = test_case.get_data()

    mock_service.repository.get_open_plan.return_value = expected_plan

    result = mock_service.get_current(user)
    assert result == expected_plan

    mock_service.repository.get_open_plan.assert_called_once()
