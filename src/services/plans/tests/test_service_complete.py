import dataclasses
from unittest.mock import MagicMock

import pytest

from src.common.testcase import TestCaseBase
from src.models.user import User


@dataclasses.dataclass(frozen=True)
class TestCase(TestCaseBase):
    user: User
    real_complete_count: int


@pytest.mark.parametrize(
    "test_case",
    [
        TestCase(
            user=User(666),
            real_complete_count=5
        ),
    ]
)
def test_service_complete_success(mock_service, test_case):
    user, real_complete_count = test_case.get_data()

    mock_service.repository.complete_open_plan = MagicMock()

    mock_service.complete_current(user, real_complete_count)
