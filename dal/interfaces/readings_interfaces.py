from abc import abstractmethod

from ..db_models import Readings
from .base_interfaces import IBaseRepository


class IReadingsRepository(IBaseRepository[Readings]):
    @abstractmethod
    async def get_between_dates(self, start, end, limit, offset):
        pass

    @abstractmethod
    async def get_by_organization(self, organization_id):
        pass

    @abstractmethod
    async def get_by_id_and_organization(self, id, organization_id):
        pass
