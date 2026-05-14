from abc import abstractmethod

from ..db_models import Users
from .base_interfaces import IBaseRepository


class IUsersRepository(IBaseRepository[Users]):
    pass

    @abstractmethod
    async def get_user_by_username(self, username: str):
        pass
