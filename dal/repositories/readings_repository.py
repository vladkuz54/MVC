from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .. import Session
from ..db_models import Readings, Sensors
from ..interfaces.readings_interfaces import IReadingsRepository
from .base_repository import BaseRepository


class ReadingsRepository(IReadingsRepository, BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, Readings)

    async def get_between_dates(
        self, start: datetime, end: datetime, limit: int, offset: int
    ):
        query = (
            select(self.model)
            .filter(self.model.timestamp.between(start, end))
            .options(joinedload(self.model.sensor).joinedload(Sensors.device))
            .limit(limit)
            .offset(offset)
            .order_by(self.model.timestamp.desc())
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_organization(self, organization_id):
        query = (
            select(self.model)
            .join(Sensors)
            .join(Sensors.device_id)
            .where(Sensors.device_id.organization_id == organization_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
