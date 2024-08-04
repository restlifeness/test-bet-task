
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.bets.schemas import CreateBet, BetResponse
from src.dependencies import get_session
from src.modules.bets.services import BetsService
from src.modules.events.models import ExternalEvent
from src.modules.events.services import ExternalEventsService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_bet(data: CreateBet, session: Annotated[AsyncSession, Depends(get_session)]) -> BetResponse:
    """Create a new bet."""
    event: ExternalEvent | None = await ExternalEventsService(session).get_by_id(data.event_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id id={event.id} not found",
        )

    return await BetsService(session).create(event, data)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_bets(
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: int = 30,
) -> list[BetResponse]:
    """Pagination for bets."""
    return await BetsService(session).get_bets(offset, limit)
