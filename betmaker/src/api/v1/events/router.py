
from fastapi import APIRouter

from .routes import crud


router = APIRouter(
    prefix="/events",
    tags=["events"],
)

router.include_router(crud.router)
