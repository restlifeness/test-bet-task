import pytest

from typing import Any
from decimal import Decimal

from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.events.enums import ExternalEventStatus
from src.modules.events.models import ExternalEvent
from src.common.time import utc_now
from tests.integration.fixtures import sqlite_session, test_client


@pytest.mark.asyncio
async def test_get_all(test_client: TestClient, sqlite_session: AsyncSession):
    """Test Get All Events"""
    events_db = [
        ExternalEvent(
            name="Test Event #1",
            odds=Decimal("1.23"),
            deadline=(utc_now() + timedelta(days=1)),
            status=ExternalEventStatus.OPEN,
        ),
        ExternalEvent(
            name="Test Event #2",
            odds=Decimal("1.23"),
            deadline=(utc_now() + timedelta(days=1)),
            status=ExternalEventStatus.OPEN,
        ),
    ]
    bad_event = ExternalEvent(
        name="Test Event #3",
        odds=Decimal("1.23"),
        deadline=(utc_now() - timedelta(days=1)),
        status=ExternalEventStatus.FIRST_TEAM_WIN,
    )
    events_db.append(bad_event)

    sqlite_session.add_all(events_db)
    await sqlite_session.commit()

    resp = test_client.get('/api/v1/events/', params={'offset': 0, 'limit': 100})

    assert resp.status_code == 200
    data = resp.json()

    assert data is not None
    assert len(data) == 2

    # NOTE: check for only open events in response
    data_ids = [item['id'] for item in data]
    db_ids = [item.id for item in events_db if item.status == ExternalEventStatus.OPEN]
    db_bad_id = bad_event.id

    assert data_ids == db_ids
    assert db_bad_id not in data_ids
