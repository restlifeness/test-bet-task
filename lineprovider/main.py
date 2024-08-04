import uvicorn
import dramatiq
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.core.jobs import redis_broker
from src.core.config import ALLOWED_ORIGINS

from src.api.v1.router import API_V1_ROUTER
from src.modules.events.exceptions import EventModuleException


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

log = logging.getLogger(__name__)


log.info("Setting up broker...")
dramatiq.set_broker(redis_broker)
log.info("COMPLETE")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(API_V1_ROUTER)


@app.exception_handler(EventModuleException)
def exception_handler(request: Request, exc: EventModuleException):
    return JSONResponse({
        "details": str(exc),
    }, status_code=400)


def main() -> None:
    log.warning('Starting FastAPI server in dev mode...')
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
