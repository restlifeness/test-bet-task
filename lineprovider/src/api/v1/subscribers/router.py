
from fastapi import APIRouter

from src.api.v1.subscribers.routes import crud


router = APIRouter(
    prefix="/subscribers",
    tags=["subscribers"],
)

router.include_router(crud.router)
