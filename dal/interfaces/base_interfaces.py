from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IBaseRepository(ABC, Generic[T]):

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, id):
        pass

    @abstractmethod
    async def create(self, obj):
        pass

    @abstractmethod
    async def update(self, obj):
        pass

    @abstractmethod
    async def delete(self, id):
        pass
