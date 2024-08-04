
from fastapi import APIRouter

from .events.router import router as events_router
from .subscribers.router import router as subscribers_router


API_V1_ROUTER = APIRouter(
    tags=['v1'],
    prefix='/api/v1',
)

API_V1_ROUTER.include_router(events_router)
API_V1_ROUTER.include_router(subscribers_router)


__all__ = [
    'API_V1_ROUTER',
]
