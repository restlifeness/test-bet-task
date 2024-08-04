
from decimal import Decimal
from datetime import datetime

from sqlalchemy import (
    Text,
    Numeric,
    DateTime,
    Enum,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.database.models import CreateUpdateMixin, BaseModel
from src.common.time import utc_now

from .enums import EventStatus


class Event(CreateUpdateMixin, BaseModel):
    """
    Event model for storing data about an event and the winning odds.
    """

    __tablename__ = 'events'

    name: Mapped[str] = mapped_column(Text, nullable=False, comment='Event name')
    odds: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment='Event odds')
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment='Event deadline')
    status: Mapped[EventStatus] = mapped_column(
        Enum(EventStatus),
        default=EventStatus.OPEN,
        nullable=False,
        comment='Event status'
    )

    @property
    def title(self) -> str:
        """Display title with odds in format `{name} x{odds}`"""
        return f"{self.name} x{self.odds}"

    @property
    def open_statuses(self) -> list[EventStatus]:
        """Return a list of open statuses."""
        return [EventStatus.OPEN]

    @property
    def closed_statuses(self) -> list[EventStatus]:
        """Return a list of closed statuses"""
        return [EventStatus.FIRST_TEAM_WIN, EventStatus.SECOND_TEAM_WIN]

    def is_ended(self) -> bool:
        """Return True if event is ended."""
        return self.deadline < utc_now()
