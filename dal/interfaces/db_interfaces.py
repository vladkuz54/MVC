from abc import ABC, abstractmethod


class IDBModels(ABC):

    @abstractmethod
    async def init_db(self):
        pass

    @abstractmethod
    async def drop_db(self):
        pass


class IDBRepository(ABC):

    @abstractmethod
    async def paste_all(self):
        pass
