import dataclasses

import pytest
import datetime as dt

from src.common.testcase import TestCaseBase
from src.models.daily_plan import DailyPlan
from src.models.user import User


@dataclasses.dataclass(frozen=True)
class TestCase(TestCaseBase):
    user: User
    get_current_result: DailyPlan | None
    is_all_closed_expected: bool
    there_are_not_closed_expected: bool


@pytest.mark.parametrize(
    "test_case",
    [
        TestCase(
            user=User(666),
            get_current_result=DailyPlan(
                id=1,
                tg_id=666,
                date=dt.date(2020, 1, 1),
                plan="some plan",
                count=3,
            ),
            is_all_closed_expected=False,
            there_are_not_closed_expected=True
        ),
        TestCase(
            user=User(666),
            get_current_result=None,
            is_all_closed_expected=True,
            there_are_not_closed_expected=False
        )
    ]
)
def test_service_checks_success(mock_service, test_case):
    user, get_current_result, is_all_closed_expected, there_are_not_closed_expected = test_case.get_data()

    mock_service.repository.get_open_plan.return_value = get_current_result

    is_all_closed = mock_service.all_is_closed(user)
    assert is_all_closed == is_all_closed_expected

    there_are_not_closed = mock_service.not_all_is_closed(user)
    assert there_are_not_closed == there_are_not_closed_expected

    assert is_all_closed != there_are_not_closed
