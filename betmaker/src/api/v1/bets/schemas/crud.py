
from pydantic import BaseModel, Field

from src.modules.bets.enums import BetStatus


class CreateBet(BaseModel):
    amount: float = Field(..., gt=0, description="Amount of bet")
    event_id: int = Field(..., description="Event ID")


class BetResponse(BaseModel):
    id: int = Field(..., description="Bet ID")
    amount: float = Field(..., description="Amount of bet")
    status: BetStatus = Field(..., description="Status of bet")
    event_id: int = Field(..., description="Event ID", validation_alias='external_event_id')
