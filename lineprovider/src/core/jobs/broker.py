import dramatiq

from dramatiq.brokers.redis import RedisBroker
from dramatiq.middleware.asyncio import AsyncIO

from src.core.config import REDIS_URI


def setup_worker():
    redis_broker = RedisBroker(url=REDIS_URI)
    redis_broker.add_middleware(AsyncIO())

    dramatiq.set_broker(redis_broker)
