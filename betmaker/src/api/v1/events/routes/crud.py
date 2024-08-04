
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.events.schemas import ExternalEventResponse, UpdateWebhookExternalEvent
from src.api.common.schemas import SuccessResponse
from src.dependencies import get_session
from src.modules.events.services import ExternalEventsService, ExternalEventUpdateWebhookService


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_events(
    session: Annotated[AsyncSession, Depends(get_session)],
    offset: int = 0,
    limit: int = 30,
) -> list[ExternalEventResponse]:
    """Pagination for bets."""
    return await ExternalEventsService(session).get_active_external_events(offset, limit)


@router.post("/external/update")
async def update_external_event(
    data: UpdateWebhookExternalEvent,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SuccessResponse:
    """Update an external event."""
    return await ExternalEventUpdateWebhookService(session).update_from_webhook(data)
