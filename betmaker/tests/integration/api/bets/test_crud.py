import pytest

from decimal import Decimal

from datetime import timedelta
from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.bets.models import Bet
from src.modules.events.models import ExternalEvent
from src.common.time import utc_now
from tests.integration.fixtures import sqlite_session, test_client


@pytest.fixture(scope="function")
async def event_db(sqlite_session: AsyncSession):
    event_db = ExternalEvent(
        name='Test Event',
        external_id=1,
        odds=Decimal("1.23"),
        deadline=utc_now() + timedelta(days=1),
    )

    sqlite_session.add(event_db)
    await sqlite_session.commit()
    return event_db


@pytest.mark.asyncio
async def test_create_bets(test_client: TestClient, event_db: ExternalEvent, sqlite_session: AsyncSession) -> None:
    event_id = event_db.id

    resp = test_client.post(
        'api/v1/bets',
        json={
            'event_id': event_id,
            'amount': 50_000,
        }
    )

    sqlite_session.expire_all()

    assert resp.status_code == 201
    data = resp.json()
    bet_id: int = data['id']

    bet_db: Bet | None = await sqlite_session.get(Bet, bet_id)

    assert bet_db is not None
    assert bet_db.amount == 50_000
    assert bet_db.external_event_id == event_id


@pytest.mark.asyncio
async def test_get_bets(test_client: TestClient, event_db: ExternalEvent, sqlite_session: AsyncSession) -> None:
    event_id = event_db.id

    bets_db = [
        Bet(amount=Decimal(50_000.00), external_event_id=event_id),
        Bet(amount=Decimal(150_000.00), external_event_id=event_id),
        Bet(amount=Decimal(1_000_000.00), external_event_id=event_id),
    ]

    sqlite_session.add_all(bets_db)
    await sqlite_session.commit()

    resp = test_client.get('/api/v1/bets', params={'offset': 0, 'limit': 100})

    assert resp.status_code == 200

    data = resp.json()

    assert len(data) == len(bets_db)

    resp_ids = [item['id'] for item in data]
    db_ids = [item.id for item in bets_db]

    assert resp_ids == db_ids
