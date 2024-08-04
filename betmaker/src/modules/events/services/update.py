
from src.core.services import AsyncSessionService
from src.core.mapper import SchemaToDatabaseMapper

from src.modules.events.repositories import ExternalEventsRepository
from src.modules.events.models import ExternalEvent
from src.modules.bets.services import BetsService
from src.api.v1.events.schemas import UpdateWebhookExternalEvent
from src.api.common.schemas import SuccessResponse


class ExternalEventUpdateWebhookService(AsyncSessionService):
    bets_service: BetsService
    mapper: SchemaToDatabaseMapper

    def __post_init__(self) -> None:
        self.repo = ExternalEventsRepository(ExternalEvent, self.session)
        self.bets_service = BetsService(self.session)
        self.mapper = SchemaToDatabaseMapper()

    async def update_from_webhook(self, data: UpdateWebhookExternalEvent) -> SuccessResponse:
        """Update external event from webhook"""
        event: ExternalEvent | None = await self.repo.get_from_external_event_id(data.id, load_bets=True)

        if not event:
            await self.repo.create(ExternalEvent(
                external_id=data.id,
                **data.model_dump(exclude={'id'}),
            ))
            return SuccessResponse(
                success=True,
            )

        event = self.mapper.map(data, event, exclude={'id'})
        await self.repo.save()

        await self.bets_service.update_after_event_update(event)

        return SuccessResponse(
            success=True,
        )
