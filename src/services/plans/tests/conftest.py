from unittest.mock import MagicMock

import pytest

from src.services.plans.service import DailyPlansService
from src.storage.postgres.repositories.daily_plans.repository import DailyPlansRepository


@pytest.fixture
def mock_service():
    service = DailyPlansService(repository=None)
    service.repository = MagicMock()
    return service
