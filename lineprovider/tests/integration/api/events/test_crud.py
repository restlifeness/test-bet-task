from typing import Any

import pytest

from datetime import timedelta
from fastapi.testclient import TestClient

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.events.models import Event
from src.common.time import utc_now
from tests.integration.fixtures import sqlite_session, test_client


@pytest.mark.asyncio
async def test_create(test_client: TestClient, sqlite_session: AsyncSession):
    """Test Create Event"""
    resp = test_client.post(
        "/api/v1/events",
        json={
            "name": "Test Event #1",
            "odds": 1.23,
            "deadline": utc_now() + timedelta(days=1),
        },
    )

    assert resp.status_code == 201

    resp_data: dict[str, Any] = await resp.json()

    event_db: Event | None = (await sqlite_session.get(Event, resp['id']))

    assert event_db is not None

    assert event_db.name == resp_data['name']
    assert event_db.odds == resp_data['odds']
    assert event_db.deadline == utc_now() + timedelta(days=1)
