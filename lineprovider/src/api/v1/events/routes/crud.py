
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies import get_session
from src.modules.events.models import Event

from src.modules.events.services import EventsService
from src.api.v1.events.schemas import (
    EventCreate,
    EventUpdate,
    EventPatch,
    EventResponse,
)


router = APIRouter(
    tags=["events"],
    dependencies=[Depends(get_session)]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_event(
    data: EventCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> EventResponse:
    """Creates a new event."""
    return await EventsService(session).create(data)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_events(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> list[EventResponse]:
    """Gets events."""
    return await EventsService(session).get_all()


@router.get("/{_id}", status_code=status.HTTP_200_OK)
async def get_event_by_id(
    _id: int,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> EventResponse:
    """Gets event by id."""
    return await EventsService(session).get_by_id(_id)


@router.put("/{_id}", status_code=status.HTTP_200_OK)
async def update_event(
    _id: int,
    data: EventUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> EventResponse:
    """Updates a event."""
    service = EventsService(session)

    event: Event | None = await service.get_by_id(_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {_id} does not exist."
        )

    return await service.update(event, data)


@router.patch("/{_id}", status_code=status.HTTP_200_OK)
async def update_event_by_id(
    _id: int,
    data: EventPatch,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> EventResponse:
    """Patch an existing event."""
    service = EventsService(session)

    event: Event | None = await service.get_by_id(_id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {_id} does not exist."
        )

    return await service.patch(event, data)
