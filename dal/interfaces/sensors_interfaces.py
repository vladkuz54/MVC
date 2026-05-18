from abc import abstractmethod

from ..db_models import Sensors
from .base_interfaces import IBaseRepository


class ISensorsRepository(IBaseRepository[Sensors]):

    @abstractmethod
    async def get_by_organization(self, organization_id):
        pass

    @abstractmethod
    async def get_by_id_and_organization(self, id, organization_id):
        pass
