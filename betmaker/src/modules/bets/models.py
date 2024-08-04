import typing

from decimal import Decimal
from datetime import datetime

from sqlalchemy import (
    Text,
    Numeric,
    DateTime,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.database.models import CreateUpdateMixin, BaseModel

from .enums import BetStatus

if typing.TYPE_CHECKING:
    from src.modules.events.models import ExternalEvent


class Bet(CreateUpdateMixin, BaseModel):
    __tablename__ = 'bets'

    amount: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False, comment='Bet amount')
    status: Mapped[BetStatus] = mapped_column(Enum(BetStatus), nullable=False, default=BetStatus.PLACED)

    external_event_id: Mapped[int] = mapped_column(ForeignKey('external_events.id'), nullable=False, comment='External event id')
    external_event: Mapped['ExternalEvent'] = relationship("ExternalEvent", back_populates="bets")
