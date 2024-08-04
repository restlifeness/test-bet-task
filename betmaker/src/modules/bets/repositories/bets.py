
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Sequence

from src.core.repositories import Repository

from src.modules.bets.models import Bet


class BetsRepository(Repository[Bet]):
    async def get_bets(
        self,
        offset: int = 0,
        limit: int = 30,
    ) -> Sequence[Bet]:
        query = (
            select(Bet)
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)

        return result.scalars().all()
