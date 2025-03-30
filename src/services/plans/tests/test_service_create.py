import dataclasses

import pytest
import datetime as dt

from src.common.testcase import TestCaseBase
from src.models.daily_plan import DailyPlanCreate
from src.models.user import User
from src.services.plans.errors import NeedPlanErr, NeedCountErr, NeedDateErr, ThereIsOpenPlanErr


@dataclasses.dataclass(frozen=True)
class TestCase(TestCaseBase):
    user: User
    plan: DailyPlanCreate
    exception: Exception | None = None


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
def test_service_create_success(mock_service, test_case):
    user, plan, _ = test_case.get_data()

    mock_service.repository.create.return_value = plan
    mock_service.repository.get_open_plan.return_value = None

    mock_service.create(user, plan)


@pytest.mark.parametrize(
    "test_case",
    [
        TestCase(
            user=User(666),
            plan=DailyPlanCreate(

            ),
            exception=NeedPlanErr
        ),
        TestCase(
            user=User(666),
            plan=DailyPlanCreate(
                count=5,
            ),
            exception=NeedPlanErr
        ),
        TestCase(
            user=User(666),
            plan=DailyPlanCreate(
                date=dt.datetime(2023, 10, 1),
            ),
            exception=NeedPlanErr
        ),
        TestCase(
            user=User(666),
            plan=DailyPlanCreate(
                count=5,
                date=dt.datetime(2023, 10, 1),
            ),
            exception=NeedPlanErr
        ),
        TestCase(
            user=User(666),
            plan=DailyPlanCreate(
                plan="Test plan 1",
            ),
            exception=NeedCountErr
        ),
        TestCase(
            user=User(666),
            plan=DailyPlanCreate(
                plan="Test plan 1",
                date=dt.datetime(2023, 10, 1),
            ),
            exception=NeedCountErr
        ),
        TestCase(
            user=User(666),
            plan=DailyPlanCreate(
                plan="Test plan 1",
                count=5,
            ),
            exception=NeedDateErr
        ),
    ],
)
def test_service_create_err_validate(mock_service, test_case):
    user, plan, exception = test_case.get_data()

    mock_service.repository.create.return_value = plan
    mock_service.repository.get_open_plan.return_value = None

    with pytest.raises(exception):
        mock_service.create(user, plan)


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
            exception=ThereIsOpenPlanErr
        ),
    ],
)
def test_service_create_err_cannot_create(mock_service, test_case):
    user, plan, exception = test_case.get_data()

    mock_service.repository.create.return_value = plan
    mock_service.repository.get_open_plan.return_value = plan

    with pytest.raises(exception):
        mock_service.create(user, plan)
