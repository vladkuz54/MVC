from abc import ABC, abstractmethod


class ISensorsService(ABC):

    @abstractmethod
    async def get_all(self):
        pass

    @abstractmethod
    async def get_by_id(self, id):
        pass

    @abstractmethod
    async def get_by_organization(self, organization_id):
        pass

    @abstractmethod
    async def get_by_id_and_organization(self, id, organization_id):
        pass

    @abstractmethod
    async def create(self, data, organization_id, role):
        pass

    @abstractmethod
    async def update(self, id, data, organization_id, role):
        pass

    @abstractmethod
    async def delete(self, id, organization_id, role):
        pass
