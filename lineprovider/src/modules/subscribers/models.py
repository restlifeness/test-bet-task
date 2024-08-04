
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
from .enums import SubscriberStatus, SubscriberStopReason


class UpdateSubscriber(BaseModel, CreateUpdateMixin):
    __tablename__ = "update_subscribers"

    status: Mapped[SubscriberStatus] = mapped_column(
        Enum(SubscriberStatus),
        index=True,
        default=SubscriberStatus.ACTIVE
    )
    stop_reason: Mapped[SubscriberStopReason | None] = mapped_column(
        Enum(SubscriberStopReason),
        nullable=True,
        default=None
    )

    callback_url: Mapped[str] = mapped_column(Text, nullable=False)
