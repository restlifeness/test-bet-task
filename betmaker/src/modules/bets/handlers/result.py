
from src.modules.bets.models import Bet
from src.modules.bets.enums import BetStatus

from src.modules.events.models import ExternalEvent
from src.modules.events.enums import ExternalEventStatus


class BetResultHandler:

    STATUS_MAP: dict[ExternalEventStatus, BetStatus] = {
        ExternalEventStatus.OPEN: BetStatus.PLACED,
        ExternalEventStatus.FIRST_TEAM_WIN: BetStatus.WON,
        ExternalEventStatus.SECOND_TEAM_WIN: BetStatus.LOST,
    }

    def __init__(self, target_event: ExternalEvent) -> None:
        """
        Bet result handler

        :param target_event: event of bets
        """
        self._target_event = target_event

    def _verify(self, bet: Bet) -> bool:
        """Check that bet event is target event"""
        return bet.external_event_id == self._target_event.id

    def _get_bet_status_by_event(self) -> BetStatus:
        """Get bet status by event"""
        return self.STATUS_MAP[self._target_event.status]

    def update_status(self, bet: Bet) -> Bet | None:
        """
        Update bet status
        
        :param bet: bet object for target event
        :return: updated bet object or none
        """
        if not self._verify(bet):
            raise ValueError(f"Bet id={bet.id} is not for event id={self._target_event.id}")

        bet.status = self._get_bet_status_by_event()

        return bet
