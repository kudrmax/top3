import dataclasses
from typing import Tuple
from unittest.mock import MagicMock

import pytest
import datetime as dt

from src.common.testcase import TestCaseBase
from src.models.daily_plan import DailyPlan
from src.models.user import User


@dataclasses.dataclass(frozen=True)
class TestCase(TestCaseBase):
    user: User
    row: Tuple | None
    result: DailyPlan | None


daily_plan_data = (
    1,
    666,
    dt.datetime(2020, 1, 1),
    "some plan",
    3,
)


@pytest.mark.parametrize(
    "test_case",
    [
        TestCase(
            user=User(666),
            row=daily_plan_data,
            result=DailyPlan(*daily_plan_data),
        ),
        TestCase(
            user=User(666),
            row=None,
            result=None,
        ),
    ],
)
def test_repository_get_last_closed_success(mock_repository, test_case):
    user, row, expected_result, = test_case.get_data()

    mock_row = MagicMock()
    mock_row.fetchone = MagicMock(return_value=row)
    mock_repository.execute = MagicMock(return_value=mock_row)

    result = mock_repository.get_open_plan(user)
    assert result == expected_result

    mock_repository.execute.assert_called_once()
