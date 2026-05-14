from sqlalchemy import select

from .. import Session
from ..db_models import Devices, Sensors
from ..interfaces.sensors_interfaces import ISensorsRepository
from .base_repository import BaseRepository


class SensorsRepository(ISensorsRepository, BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, Sensors)

    async def get_by_organization(self, organization_id):
        query = (
            select(self.model)
            .join(Devices)
            .where(Devices.organization_id == organization_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
