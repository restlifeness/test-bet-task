import pytest

from typing import Any
from decimal import Decimal

from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.events.enums import EventStatus
from src.modules.events.models import Event
from src.common.time import utc_now
from tests.integration.fixtures import sqlite_session, test_client


@pytest.fixture(scope="function")
async def event_db(sqlite_session: AsyncSession) -> Event:
    """Basic event fixture."""
    event_db: Event = Event(
        name="Test Event #1",
        odds=Decimal("1.23"),
        deadline=(utc_now() + timedelta(days=1)),
        status=EventStatus.OPEN,
    )
    sqlite_session.add(event_db)
    await sqlite_session.commit()

    return event_db


@pytest.mark.asyncio
async def test_create(test_client: TestClient, sqlite_session: AsyncSession):
    """Test Create Event"""
    resp = test_client.post(
        "/api/v1/events/",
        json={
            "name": "Test Event #1",
            "odds": 1.23,
            "deadline": (utc_now() + timedelta(days=1)).timestamp(),
        },
    )

    assert resp.status_code == 201

    resp_data: dict[str, Any] = resp.json()

    event_db: Event | None = (await sqlite_session.get(Event, resp_data['id']))

    assert event_db is not None

    assert event_db.name == resp_data['name']
    assert float(event_db.odds) == resp_data['odds']


@pytest.mark.asyncio
async def test_update(test_client: TestClient, event_db: Event, sqlite_session: AsyncSession):
    """Test Update Event"""
    event_id: int = event_db.id

    resp = test_client.put(
        f'/api/v1/events/{event_id}',
        json={
            'name': 'Updated Event #1',
            'odds': 1.55,
            'status': event_db.status,
            'deadline': event_db.deadline.timestamp(),
        },
    )

    sqlite_session.expire_all()
    event_db: Event | None = await sqlite_session.get(Event, event_id)

    assert resp.status_code == 200
    assert event_db is not None
    assert event_db.name == 'Updated Event #1'
    assert event_db.odds == Decimal("1.55")


@pytest.mark.asyncio
async def test_patch(test_client: TestClient, event_db: Event, sqlite_session: AsyncSession):
    """Test Patch Event"""
    event_id: int = event_db.id

    resp = test_client.patch(
        f'/api/v1/events/{event_id}',
        json={
            'odds': 1.55,
        }
    )

    sqlite_session.expire_all()
    event_db: Event | None = await sqlite_session.get(Event, event_id)

    assert resp.status_code == 200
    assert event_db is not None
    assert event_db.name == 'Test Event #1'
    assert event_db.odds == Decimal("1.55")


@pytest.mark.asyncio
async def test_get(test_client: TestClient, event_db: Event, sqlite_session: AsyncSession):
    """Test Get Event by id"""
    event_id: int = event_db.id

    resp = test_client.get(f'/api/v1/events/{event_id}')

    assert resp.status_code == 200

    data = resp.json()

    assert data is not None
    assert data['name'] == event_db.name
    assert data['odds'] == float(event_db.odds)


@pytest.mark.asyncio
async def test_get_all(test_client: TestClient, event_db: Event, sqlite_session: AsyncSession):
    """Test Get All Events"""

    resp = test_client.get('/api/v1/events/')

    assert resp.status_code == 200
    data = resp.json()

    assert data is not None
    assert len(data) == 1

    assert data[0]['name'] == event_db.name
    assert data[0]['odds'] == float(event_db.odds)
