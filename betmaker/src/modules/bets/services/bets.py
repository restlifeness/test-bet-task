
from typing import Sequence

from src.core.services import AsyncSessionService
from src.core.repositories import Repository

from src.modules.bets.models import Bet
from src.modules.bets.repositories import BetsRepository
from src.modules.bets.exceptions import BetToOutdatedEventError
from src.modules.bets.handlers import BetResultHandler
from src.modules.events.models import ExternalEvent

from src.api.v1.bets.schemas import CreateBet


class BetsService(AsyncSessionService):
    def __post_init__(self) -> None:
        self.repo = BetsRepository(Bet, self.session)

    async def create(self, event: ExternalEvent, data: CreateBet) -> Bet:
        """Create Bet from data"""

        if event.is_ended():
            raise BetToOutdatedEventError(f"Cannot make bet for outdated event {event.name}")

        return await self.repo.create(Bet(
            external_event_id=event.id,
            **data.model_dump(exclude={'event_id'})
        ))

    async def get_bets(self, offset: int, limit: int) -> Sequence[Bet]:
        """Get bets"""
        return await self.repo.get_bets(offset, limit)

    async def update_after_event_update(self, event: ExternalEvent) -> list[Bet]:
        """
        Update bets after event update

        :param event: event for bets to update
        :return: updated bets
        """
        handler: BetResultHandler = BetResultHandler(event)

        bets: list[Bet] = [
            handler.update_status(bet)
            for bet in event.bets
        ]

        await self.repo.save()

        return bets
