from sqlalchemy import select

from .. import Session
from ..db_models import Alerts, Devices
from ..interfaces.alerts_interfaces import IAlertsRepository
from .base_repository import BaseRepository


class AlertsRepository(IAlertsRepository, BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, Alerts)

    async def get_by_organization(self, organization_id):
        query = (
            select(self.model)
            .join(Devices)
            .where(Devices.organization_id == organization_id)
        )
        result = await self.session.execute(query)
        return result.scalars()

    async def get_by_id_and_organization(self, id, organization_id):
        query = (
            select(self.model)
            .join(Devices)
            .where(self.model.id == id, Devices.organization_id == organization_id)
        )
        result = await self.session.execute(query)
        return result.scalars().first()
