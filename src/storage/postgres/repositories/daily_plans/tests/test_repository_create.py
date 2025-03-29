import dataclasses
from unittest.mock import ANY

import pytest
import datetime as dt

from sqlalchemy.exc import IntegrityError

from src.common.testcase import TestCaseBase
from src.models.daily_plan import DailyPlanCreate
from src.models.user import User
from src.storage.postgres.repositories.base import Params
from src.storage.postgres.repositories.daily_plans.errors import PlanAlreadyExistsWithThisDateErr


@dataclasses.dataclass(frozen=True)
class TestCase(TestCaseBase):
    user: User
    plan: DailyPlanCreate


@pytest.mark.parametrize(
    "test_case",
    [
        TestCase(
            user=User(666),
            plan=DailyPlanCreate(
                plan="Test plan 1",
                count=5,
                date=dt.datetime(2023, 10, 1),
            ),
        ),
        TestCase(
            user=User(666),
            plan=DailyPlanCreate(
                plan="Test plan 2",
                count=5,
            ),
        ),
        TestCase(
            user=User(666),
            plan=DailyPlanCreate(
                plan="Test plan 3",
            ),
        ),
        TestCase(
            user=User(666),
            plan=DailyPlanCreate(),
        ),
    ],
)
def test_repository_create_success(mock_repository, test_case):
    user, plan = test_case.get_data()

    mock_repository.create(user=user, plan=plan)
    mock_repository.execute.assert_called_once()


@pytest.mark.parametrize(
    "test_case",
    [
        TestCase(
            user=User(666),
            plan=DailyPlanCreate(
                plan="Test plan 1",
                count=5,
                date=dt.datetime(2023, 10, 1),
            ),
        ),
    ],
)
def test_repository_create_err_date_already_exists(mock_repository, test_case):
    user, plan = test_case.get_data()

    mock_repository.execute.side_effect = IntegrityError("duplicate key value violates unique constraint", {}, None)

    with pytest.raises(PlanAlreadyExistsWithThisDateErr):
        mock_repository.create(user=user, plan=plan)