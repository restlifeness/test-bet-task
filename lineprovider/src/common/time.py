
from datetime import datetime
from pytz import timezone, UTC
from timezonefinder import TimezoneFinder

tf = TimezoneFinder()


def utc_now() -> datetime:
    """Returns current datetime in UTC timezone"""
    return datetime.now(tz=UTC)


def tz_now(timezone_name: str) -> datetime:
    """Returns current datetime in specified timezone"""
    return datetime.now(tz=timezone(timezone_name))


def coordinates_now(latitude: float, longitude: float) -> datetime:
    """Returns current datetime in specified coordinates"""
    tz = coordinates_timezone(latitude, longitude)
    return datetime.now(tz=timezone(tz))


def coordinates_timezone(latitude: float, longitude: float) -> str:
    """Returns timezone for specified coordinates"""
    return tf.timezone_at(lat=latitude, lng=longitude)
