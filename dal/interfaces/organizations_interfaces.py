from abc import abstractmethod

from ..db_models import Organizations
from .base_interfaces import IBaseRepository


class IOrganizationsRepository(IBaseRepository[Organizations]):

    @abstractmethod
    async def get_by_organization(self, organization_id):
        pass
