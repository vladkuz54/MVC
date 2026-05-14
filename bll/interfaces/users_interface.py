from abc import ABC, abstractmethod


class IUsersService(ABC):

    @abstractmethod
    async def get_user_by_username(self, username: str):
        pass

    @abstractmethod
    async def create(self, data):
        pass
