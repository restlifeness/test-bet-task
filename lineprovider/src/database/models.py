
from datetime import datetime
from uuid import UUID

from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy.dialects.postgresql import UUID

from src.common.time import utc_now


class BaseModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class CreateUpdateMixin:
    """Create and update timestamp mixin"""

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )


class UUIDMixin:
    """UUID Postgres mixin"""

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), index=True)
