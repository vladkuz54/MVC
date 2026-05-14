from sqlalchemy import select

from .. import Session
from ..db_models import Devices
from ..interfaces.devices_interfaces import IDevicesRepository
from .base_repository import BaseRepository


class DevicesRepository(IDevicesRepository, BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, Devices)

    async def get_by_organization(self, organization_id):
        result = await self.session.execute(
            select(self.model).where(self.model.organization_id == organization_id)
        )
        return result.scalars().first()
