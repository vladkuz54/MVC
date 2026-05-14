from pydantic import BaseModel

from dal.db_models import Sensors
from dal.interfaces.devices_interfaces import IDevicesRepository
from dal.interfaces.organizations_interfaces import IOrganizationsRepository
from dal.interfaces.sensors_interfaces import ISensorsRepository

from ..exceptions import EntityNotFoundError
from ..interfaces.sensors_interface import ISensorsService


class SensorRequest(BaseModel):
    device_id: int
    type: str
    unit: str


class SensorsService(ISensorsService):

    def __init__(
        self,
        sensors_repository: ISensorsRepository,
        devices_repository: IDevicesRepository,
        organizations_repository: IOrganizationsRepository,
    ):
        self.repository = sensors_repository
        self.devices_repository = devices_repository
        self.organizations_repository = organizations_repository

    async def get_all(self):
        return await self.repository.get_all()

    async def get_by_id(self, id):
        obj_to_get = await self.repository.get_by_id(id)
        if not obj_to_get:
            raise EntityNotFoundError(f"Sensor with ID {id} not found")
        return await self.repository.get_by_id(id)

    async def get_by_organization(self, organization_id):
        organization = await self.organizations_repository.get_by_id(organization_id)
        if not organization:
            raise EntityNotFoundError(
                f"Organization with ID {organization_id} not found"
            )
        obj_to_get = await self.repository.get_by_organization(organization_id)
        if not obj_to_get:
            raise EntityNotFoundError(
                f"Sensor for Organization ID {organization_id} not found"
            )
        return await self.repository.get_by_organization(organization_id)

    async def create(self, data: SensorRequest):
        device = await self.devices_repository.get_by_id(data.device_id)
        if not device:
            raise EntityNotFoundError(f"Device with ID {data.device_id} not found")

        obj_to_create = Sensors(
            device_id=data.device_id,
            type=data.type,
            unit=data.unit,
        )
        return await self.repository.create(obj_to_create)

    async def update(self, id, data: SensorRequest):
        obj_to_update = await self.repository.get_by_id(id)
        if not obj_to_update:
            raise EntityNotFoundError(f"Sensor with ID {id} not found")

        device = await self.devices_repository.get_by_id(data.device_id)
        if not device:
            raise EntityNotFoundError(f"Device with ID {data.device_id} not found")

        for field, value in data.model_dump().items():
            setattr(obj_to_update, field, value)
        return await self.repository.update(obj_to_update)

    async def delete(self, id):
        obj_to_delete = await self.repository.get_by_id(id)
        if not obj_to_delete:
            raise EntityNotFoundError(f"Sensor with ID {id} not found")
        return await self.repository.delete(id)
