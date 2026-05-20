from pydantic import BaseModel

from dal.db_models import Alerts
from dal.interfaces.alerts_interfaces import IAlertsRepository
from dal.interfaces.devices_interfaces import IDevicesRepository
from dal.interfaces.organizations_interfaces import IOrganizationsRepository

from ..exceptions import EntityNotFoundError
from ..interfaces.alerts_interface import IAlertsService


class AlertRequest(BaseModel):
    device_id: int
    severity: str
    message: str
    is_resolved: bool = False


class AlertsService(IAlertsService):
    def __init__(
        self,
        alerts_repository: IAlertsRepository,
        devices_repository: IDevicesRepository,
        organizations_repository: IOrganizationsRepository,
    ):
        self.alerts_repository = alerts_repository
        self.devices_repository = devices_repository
        self.organizations_repository = organizations_repository

    async def get_all(self):
        return await self.alerts_repository.get_all()

    async def get_by_id(self, id):
        obj_to_get = await self.alerts_repository.get_by_id(id)
        if not obj_to_get:
            raise EntityNotFoundError(f"Alert with ID {id} not found")
        return await self.alerts_repository.get_by_id(id)

    async def get_by_organization(self, organization_id):
        organization = await self.organizations_repository.get_by_id(organization_id)
        if not organization:
            raise EntityNotFoundError(
                f"Organization with ID {organization_id} not found"
            )
        obj_to_get = await self.alerts_repository.get_by_organization(organization_id)
        if not obj_to_get:
            raise EntityNotFoundError(
                f"Alert for Organization ID {organization_id} not found"
            )
        return await self.alerts_repository.get_by_organization(organization_id)

    async def get_by_id_and_organization(self, id, organization_id):
        organization = await self.organizations_repository.get_by_id(organization_id)
        if not organization:
            raise EntityNotFoundError(
                f"Organization with ID {organization_id} not found"
            )
        obj_to_get = await self.alerts_repository.get_by_id_and_organization(
            id, organization_id
        )
        if not obj_to_get:
            raise EntityNotFoundError(
                f"Alert with ID {id} for Organization ID {organization_id} not found"
            )
        return await self.alerts_repository.get_by_id_and_organization(
            id, organization_id
        )

    async def create(self, data: AlertRequest, organization_id: int, role: str):
        device = await self.devices_repository.get_by_id(data.device_id)
        if not device:
            raise EntityNotFoundError(f"Device with ID {data.device_id} not found")

        if role == "user":
            organization_objects = (
                await self.devices_repository.get_by_id_and_organization(
                    data.device_id, organization_id
                )
            )
            if not organization_objects:
                raise EntityNotFoundError(
                    f"Device with ID {data.device_id} not found in organization {organization_id}"
                )

        obj_to_create = Alerts(
            device_id=data.device_id,
            severity=data.severity,
            message=data.message,
            is_resolved=data.is_resolved,
        )
        return await self.alerts_repository.create(obj_to_create)

    async def update(self, id, data: AlertRequest, organization_id: int, role: str):
        obj_to_update = await self.alerts_repository.get_by_id(id)
        if not obj_to_update:
            raise EntityNotFoundError(f"Alert with ID {id} not found")

        if role == "user":
            organization_objects = (
                await self.devices_repository.get_by_id_and_organization(
                    data.device_id, organization_id
                )
            )
            if not organization_objects:
                raise EntityNotFoundError(
                    f"Device with ID {data.device_id} not found in organization {organization_id}"
                )

        device = await self.devices_repository.get_by_id(data.device_id)
        if not device:
            raise EntityNotFoundError(f"Device with ID {data.device_id} not found")

        for field, value in data.model_dump().items():
            setattr(obj_to_update, field, value)
        return await self.alerts_repository.update(obj_to_update)

    async def delete(self, id, organization_id: int, role: str):
        obj_to_delete = await self.alerts_repository.get_by_id(id)
        if not obj_to_delete:
            raise EntityNotFoundError(f"Alert with ID {id} not found")

        if role == "user":
            alert_objects = await self.alerts_repository.get_by_id_and_organization(
                id, organization_id
            )
            if not alert_objects:
                raise EntityNotFoundError(
                    f"Alert with ID {id} not found in organization {organization_id}"
                )

        return await self.alerts_repository.delete(id)
