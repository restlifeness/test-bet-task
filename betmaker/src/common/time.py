
from datetime import datetime
from pytz import timezone, utc


def utc_now() -> datetime:
    """Returns current datetime in UTC timezone"""
    return datetime.now(tz=utc)


def tz_now(timezone_name: str) -> datetime:
    """Returns current datetime in specified timezone"""
    return datetime.now(tz=timezone(timezone_name))
