
from datetime import datetime
from pydantic import BaseModel, Field

from src.modules.events.enums import ExternalEventStatus


class UpdateWebhookExternalEvent(BaseModel):
    id: int = Field(description="Event ID")
    name: str = Field(description="Event name")
    status: ExternalEventStatus = Field(description="Event status")
    odds: float = Field(description="Event odds")
    deadline: datetime = Field(description="Event deadline")
