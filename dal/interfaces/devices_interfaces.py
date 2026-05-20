from abc import abstractmethod

from ..db_models import Devices
from .base_interfaces import IBaseRepository


class IDevicesRepository(IBaseRepository[Devices]):

    @abstractmethod
    async def get_by_organization(self, organization_id):
        pass

    @abstractmethod
    async def get_by_id_and_organization(self, id, organization_id):
        pass
