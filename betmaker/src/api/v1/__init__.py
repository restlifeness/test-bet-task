
from fastapi import APIRouter

from .events import events_router


API_V1_ROUTER = APIRouter(
    tags=['v1'],
    prefix='/api/v1',
)

API_V1_ROUTER.include_router(events_router)


__all__ = [
    'API_V1_ROUTER',
]
