from abc import abstractmethod

from ..db_models import Alerts
from .base_interfaces import IBaseRepository


class IAlertsRepository(IBaseRepository[Alerts]):
    pass

    @abstractmethod
    async def get_by_organization(self, organization_id):
        pass
