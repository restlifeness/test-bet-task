
from enum import StrEnum


class SubscriberStatus(StrEnum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    STOPPED = 'STOPPED'


class SubscriberStopReason(StrEnum):
    LATENCY = 'LATENCY'
    INVALID_RESPONSE = 'INVALID_RESPONSE'
    URL_NOT_FOUND = 'URL_NOT_FOUND'
