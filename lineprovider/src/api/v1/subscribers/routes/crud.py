
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession
from src.dependencies import get_session

from src.api.v1.subscribers.schemas import UpdateSubscriberCreate, UpdateSubscriberUpdate, UpdateSubscriberResponse
from src.modules.subscribers.models import UpdateSubscriber
from src.modules.subscribers.services import SubscribersService


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_subscriber(
    data: UpdateSubscriberCreate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UpdateSubscriberResponse:
    return await SubscribersService(session).create(data)


@router.put('/{subscriber_id}', status_code=status.HTTP_200_OK)
async def put_subscriber(
    subscriber_id: int,
    data: UpdateSubscriberUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UpdateSubscriberResponse:
    service = SubscribersService(session)

    subscriber: UpdateSubscriber | None = await service.get_by_id(subscriber_id)

    if not subscriber:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Subscriber not found',
        )

    return await service.put(subscriber, data)
