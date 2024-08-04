import logging

from sqlalchemy import URL

from .secret import ENV


log = logging.getLogger(__name__)


TIMEZONE = 'Europe/Moscow'

ALLOWED_ORIGINS = [
    '*',
]

DATABASE_SETTINGS = {
    'url': URL.create(
        'postgresql+asyncpg',
        host=ENV.DB_HOST,
        port=ENV.DB_PORT,
        database=ENV.DB_NAME,
        username=ENV.DB_USER,
        password=ENV.DB_PASSWORD,
    ),

    # Pool Settings
    'pool_size': 10,
    'pool_timeout': 30,
    'pool_recycle': 300,
    'pool_pre_ping': True,  # NOTE: can be False if postgres fine-tuned

    'echo': False,
}

if '*' in ALLOWED_ORIGINS:
    log.warning('`ALLOWED_ORIGINS` contains *')
