from unittest.mock import MagicMock

import pytest

from src.storage.postgres.repositories.daily_plans.repository import DailyPlansRepository


@pytest.fixture
def mock_repository():
    repo = DailyPlansRepository(engine=None)
    repo.execute = MagicMock()
    yield repo
    repo.execute.reset_mock()
