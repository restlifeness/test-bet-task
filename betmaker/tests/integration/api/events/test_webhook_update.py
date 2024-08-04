
import pytest

from typing import Any
from decimal import Decimal

from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.events.enums import ExternalEventStatus
from src.modules.events.models import ExternalEvent
from src.modules.bets.models import Bet
from src.modules.bets.enums import BetStatus
from src.common.time import utc_now
from tests.integration.fixtures import sqlite_session, test_client


@pytest.fixture(scope="function")
async def event_db(sqlite_session: AsyncSession) -> ExternalEvent:
    event_db = ExternalEvent(
        external_id=1,
        name="Test Event #2",
        odds=Decimal("1.23"),
        deadline=(utc_now() + timedelta(days=1)),
        status=ExternalEventStatus.OPEN,
    )
    sqlite_session.add(event_db)
    await sqlite_session.commit()
    return event_db


@pytest.mark.asyncio
async def test_create_external_event_from_webhook(test_client: TestClient, sqlite_session: AsyncSession) -> None:
    """Test create external event from webhook."""

    external_event_id = 1
    resp = test_client.post(
        'api/v1/events/external/update/',
        json={
            'id': external_event_id,
            'name': "Test Event Name #1",
            'odds': 1.23,
            'deadline': (utc_now() + timedelta(days=3)).timestamp(),
            'status': ExternalEventStatus.OPEN,
        }
    )

    assert resp.status_code == 200

    event_db: ExternalEvent | None = (await sqlite_session.execute(
        select(ExternalEvent)
        .where(ExternalEvent.id == external_event_id)
    )).scalars().one_or_none()

    assert event_db is not None

    assert event_db.name == "Test Event Name #1"
    assert float(event_db.odds) == 1.23
    assert event_db.status == ExternalEventStatus.OPEN


@pytest.mark.asyncio
async def test_update_external_event_with_bets_won_effect_from_webhook(
    test_client: TestClient,
    event_db: ExternalEvent,
    sqlite_session: AsyncSession
):
    """Test update external event from webhook."""
    external_event_id = event_db.external_id
    event_id = event_db.id

    bet_db = Bet(amount=Decimal(50_000.00), external_event_id=event_id)
    sqlite_session.add(bet_db)

    await sqlite_session.commit()
    bet_id = bet_db.id

    resp = test_client.post(
        'api/v1/events/external/update/',
        json={
            'id': external_event_id,
            'name': event_db.name,
            'odds': float(event_db.odds),
            'deadline': event_db.deadline.timestamp(),
            'status': ExternalEventStatus.FIRST_TEAM_WIN,
        }
    )

    assert resp.status_code == 200

    sqlite_session.expire_all()

    updated_event_db = await sqlite_session.get(ExternalEvent, event_id)
    updated_bet_db = await sqlite_session.get(Bet, bet_id)

    # NOTE: check updated status
    assert updated_event_db.status == ExternalEventStatus.FIRST_TEAM_WIN

    # NOTE: check updated bets
    assert updated_bet_db.status == BetStatus.WON


@pytest.mark.asyncio
async def test_update_external_event_with_bets_lost_effect_from_webhook(
    test_client: TestClient,
    event_db: ExternalEvent,
    sqlite_session: AsyncSession
):
    """Test update external event from webhook."""
    external_event_id = event_db.external_id
    event_id = event_db.id

    bet_db = Bet(amount=Decimal(50_000.00), external_event_id=event_id)
    sqlite_session.add(bet_db)

    await sqlite_session.commit()
    bet_id = bet_db.id

    resp = test_client.post(
        'api/v1/events/external/update/',
        json={
            'id': external_event_id,
            'name': event_db.name,
            'odds': float(event_db.odds),
            'deadline': event_db.deadline.timestamp(),
            'status': ExternalEventStatus.SECOND_TEAM_WIN,
        }
    )

    assert resp.status_code == 200

    sqlite_session.expire_all()

    updated_event_db = await sqlite_session.get(ExternalEvent, event_id)
    updated_bet_db = await sqlite_session.get(Bet, bet_id)

    # NOTE: check updated status
    assert updated_event_db.status == ExternalEventStatus.SECOND_TEAM_WIN

    # NOTE: check updated bets
    assert updated_bet_db.status == BetStatus.LOST


@pytest.mark.asyncio
async def test_update_external_event_without_bets_effect_from_webhook(
    test_client: TestClient,
    event_db: ExternalEvent,
    sqlite_session: AsyncSession
):
    """Test update external event from webhook."""
    external_event_id = event_db.external_id
    event_id = event_db.id

    bet_db = Bet(amount=Decimal(50_000.00), external_event_id=event_id)
    sqlite_session.add(bet_db)

    await sqlite_session.commit()
    bet_id = bet_db.id

    resp = test_client.post(
        'api/v1/events/external/update/',
        json={
            'id': external_event_id,
            'name': "updated",
            'odds': float(event_db.odds),
            'deadline': event_db.deadline.timestamp(),
            'status': ExternalEventStatus.OPEN,
        }
    )

    assert resp.status_code == 200

    sqlite_session.expire_all()

    updated_event_db = await sqlite_session.get(ExternalEvent, event_id)
    updated_bet_db = await sqlite_session.get(Bet, bet_id)

    # NOTE: check updated name
    assert updated_event_db.name == "updated"

    # NOTE: check bets not updated
    assert updated_bet_db.status == BetStatus.PLACED
