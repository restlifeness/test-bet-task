import typing

from decimal import Decimal
from datetime import datetime

from sqlalchemy import (
    Integer,
    Text,
    Numeric,
    DateTime,
    Enum,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.database.models import CreateUpdateMixin, BaseModel
from src.common.time import utc_now, safe_utc

from .enums import ExternalEventStatus

if typing.TYPE_CHECKING:
    from src.modules.bets.models import Bet


class ExternalEvent(BaseModel, CreateUpdateMixin):
    __tablename__ = "external_events"

    external_id = mapped_column(Integer, index=True, unique=True)

    name: Mapped[str] = mapped_column(Text, nullable=False, comment='Event name')
    odds: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, comment='Event odds')
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, comment='Event deadline')
    status: Mapped[ExternalEventStatus] = mapped_column(
        Enum(ExternalEventStatus),
        default=ExternalEventStatus.OPEN,
        nullable=False,
        comment='Event status'
    )

    bets: Mapped[list['Bet']] = relationship("Bet", back_populates="external_event")

    def is_ended(self) -> bool:
        """Return True if event is ended."""
        return safe_utc(self.deadline) < utc_now()
