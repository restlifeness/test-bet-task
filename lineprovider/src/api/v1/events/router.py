
from fastapi import APIRouter

from src.api.v1.events.routes import crud


router = APIRouter(
    prefix="/events",
    tags=['events'],
)

router.include_router(crud.router)
