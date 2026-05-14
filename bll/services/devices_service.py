from pydantic import BaseModel

from dal.db_models import Devices
from dal.interfaces.devices_interfaces import IDevicesRepository
from dal.interfaces.organizations_interfaces import IOrganizationsRepository

from ..exceptions import EntityNotFoundError
from ..interfaces.devices_interface import IDevicesService


class DeviceRequest(BaseModel):
    organization_id: int
    mac_address: str
    status: str
    firmware_version: str


class DevicesService(IDevicesService):
    def __init__(
        self,
        devices_repository: IDevicesRepository,
        organizations_repository: IOrganizationsRepository,
    ):
        self.devices_repository = devices_repository
        self.organizations_repository = organizations_repository

    async def get_all(self):
        return await self.devices_repository.get_all()

    async def get_by_id(self, id):
        obj_to_get = await self.devices_repository.get_by_id(id)
        if not obj_to_get:
            raise EntityNotFoundError(f"Device with ID {id} not found")
        return await self.devices_repository.get_by_id(id)

    async def get_by_organization(self, organization_id):
        organization = await self.organizations_repository.get_by_id(organization_id)
        if not organization:
            raise EntityNotFoundError(
                f"Organization with ID {organization_id} not found"
            )
        obj_to_get = await self.devices_repository.get_by_organization(organization_id)
        if not obj_to_get:
            raise EntityNotFoundError(
                f"Device for Organization ID {organization_id} not found"
            )
        return await self.devices_repository.get_by_organization(organization_id)

    async def create(self, data: DeviceRequest):
        org = await self.organizations_repository.get_by_id(data.organization_id)
        if not org:
            raise EntityNotFoundError(
                f"Organization with ID {data.organization_id} not found"
            )

        obj_to_create = Devices(
            organization_id=data.organization_id,
            mac_address=data.mac_address,
            status=data.status,
            firmware_version=data.firmware_version,
        )
        return await self.devices_repository.create(obj_to_create)

    async def update(self, id, data: DeviceRequest):
        obj_to_update = await self.devices_repository.get_by_id(id)
        if not obj_to_update:
            raise EntityNotFoundError(f"Device with ID {id} not found")

        org = await self.organizations_repository.get_by_id(data.organization_id)
        if not org:
            raise EntityNotFoundError(
                f"Organization with ID {data.organization_id} not found"
            )

        for field, value in data.model_dump().items():
            setattr(obj_to_update, field, value)
        return await self.devices_repository.update(obj_to_update)

    async def delete(self, id):
        obj_to_delete = await self.devices_repository.get_by_id(id)
        if not obj_to_delete:
            raise EntityNotFoundError(f"Device with ID {id} not found")
        return await self.devices_repository.delete(id)
