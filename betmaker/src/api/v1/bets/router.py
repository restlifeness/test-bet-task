
from fastapi import APIRouter

from .routes import crud


router = APIRouter(
    prefix="/bets",
    tags=["bets"],
)

router.include_router(crud.router)
