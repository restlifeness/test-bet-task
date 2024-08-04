
from pydantic import BaseModel, Field


class UpdateSubscriberSchema(BaseModel):
    callback_url: str = Field(..., description="URL to receive updates")


class UpdateSubscriberCreate(UpdateSubscriberSchema):
    ...


class UpdateSubscriberUpdate(UpdateSubscriberSchema):
    ...


class UpdateSubscriberResponse(BaseModel):
    id: int = Field(..., description="The id of the subscriber")
