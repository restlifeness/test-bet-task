
from datetime import datetime
from pydantic import BaseModel, Field

from src.api.common.schemas import PatchModel
from src.modules.events.enums import EventStatus


class EventCreate(BaseModel):
    name: str = Field(description="Event name")
    odds: float = Field(description="Event odds")
    deadline: datetime = Field(description="Event deadline")


class EventResponse(BaseModel):
    id: int = Field(description="Event ID")
    name: str = Field(description="Event name")
    status: EventStatus = Field(description="Event status")
    odds: float = Field(description="Event odds")
    deadline: datetime = Field(description="Event deadline")


class EventUpdate(EventCreate):
    status: EventStatus = Field(description="Event status")


class EventPatch(PatchModel):
    name: str | None = Field(None, description="Event name")
    status: EventStatus | None = Field(None, description="Event status")
    odds: float | None = Field(None, description="Event odds")
    deadline: datetime | None = Field(None, description="Event deadline")
