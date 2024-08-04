import uvicorn
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import API_V1_ROUTER

from src.core.config import ALLOWED_ORIGINS


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

log = logging.getLogger(__name__)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(API_V1_ROUTER)


def main() -> None:
    log.warning('Starting FastAPI server in dev mode...')
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
