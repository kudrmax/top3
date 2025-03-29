import dataclasses
from unittest.mock import MagicMock

import pytest
import datetime as dt

from src.common.testcase import TestCaseBase
from src.models.daily_plan import DailyPlan
from src.models.user import User
from src.storage.postgres.repositories.daily_plans.errors import OpenPlanNotFoundErr


@dataclasses.dataclass(frozen=True)
class TestCase(TestCaseBase):
    user: User
    real_complete_count: int
    current_plan: DailyPlan | None


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
            real_complete_count=3,
            current_plan=DailyPlan(*daily_plan_data),
        ),
    ],
)
def test_repository_complete_success(mock_repository, test_case):
    user, real_complete_count, current_plan, = test_case.get_data()

    mock_repository.get_open_plan = MagicMock(return_value=current_plan)
    mock_repository.get_open_plan(user)

    mock_repository.complete_open_plan(user, real_complete_count)
    mock_repository.execute.assert_called_once()


@pytest.mark.parametrize(
    "test_case",
    [
        TestCase(
            user=User(666),
            real_complete_count=3,
            current_plan=None,
        ),
    ],
)
def test_repository_complete_err_no_open_plans(mock_repository, test_case):
    user, real_complete_count, current_plan, = test_case.get_data()

    mock_repository.get_open_plan = MagicMock(return_value=current_plan)
    mock_repository.get_open_plan(user)

    with pytest.raises(OpenPlanNotFoundErr):
        mock_repository.complete_open_plan(user, real_complete_count)
    mock_repository.execute.assert_not_called()
