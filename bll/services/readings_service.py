from datetime import datetime

from pydantic import BaseModel

from dal.db_models import Readings
from dal.interfaces.organizations_interfaces import IOrganizationsRepository
from dal.interfaces.readings_interfaces import IReadingsRepository
from dal.interfaces.sensors_interfaces import ISensorsRepository

from ..exceptions import EntityNotFoundError
from ..interfaces.readings_interface import IReadingsService


class ReadingRequest(BaseModel):
    sensor_id: int
    value: float


class ReadingsService(IReadingsService):

    def __init__(
        self,
        readings_repository: IReadingsRepository,
        sensors_repository: ISensorsRepository,
        organizations_repository: IOrganizationsRepository,
    ):
        self.readings_repository = readings_repository
        self.sensors_repository = sensors_repository
        self.organizations_repository = organizations_repository

    async def get_all(self):
        return await self.readings_repository.get_all()

    async def get_by_id(self, id):
        obj_to_get = await self.readings_repository.get_by_id(id)
        if not obj_to_get:
            raise EntityNotFoundError(f"Reading with ID {id} not found")
        return await self.readings_repository.get_by_id(id)

    async def get_between_dates(
        self, start: datetime, end: datetime, limit: int, offset: int
    ):
        return await self.readings_repository.get_between_dates(
            start, end, limit, offset
        )

    async def get_by_organization(self, organization_id):
        organization = await self.organizations_repository.get_by_id(organization_id)
        if not organization:
            raise EntityNotFoundError(
                f"Organization with ID {organization_id} not found"
            )
        obj_to_get = await self.readings_repository.get_by_organization(organization_id)
        if not obj_to_get:
            raise EntityNotFoundError(
                f"Reading for Organization ID {organization_id} not found"
            )
        return await self.readings_repository.get_by_organization(organization_id)

    async def get_by_id_and_organization(self, id, organization_id):
        organization = await self.organizations_repository.get_by_id(organization_id)
        if not organization:
            raise EntityNotFoundError(
                f"Organization with ID {organization_id} not found"
            )
        obj_to_get = await self.readings_repository.get_by_id_and_organization(
            id, organization_id
        )
        if not obj_to_get:
            raise EntityNotFoundError(
                f"Reading with ID {id} for Organization ID {organization_id} not found"
            )
        return await self.readings_repository.get_by_id_and_organization(
            id, organization_id
        )

    async def create(self, data: ReadingRequest, organization_id: int, role: str):
        sensor = await self.sensors_repository.get_by_id(data.sensor_id)
        if not sensor:
            raise EntityNotFoundError(f"Sensor with ID {data.sensor_id} not found")

        if role == "user":
            sensor = await self.sensors_repository.get_by_id_and_organization(
                data.sensor_id, organization_id
            )
            if not sensor:
                raise EntityNotFoundError(
                    f"Sensor with ID {data.sensor_id} not found in organization {organization_id}"
                )

        obj_to_create = Readings(
            sensor_id=data.sensor_id,
            value=data.value,
        )
        return await self.readings_repository.create(obj_to_create)

    async def update(self, id, data: ReadingRequest, organization_id: int, role: str):
        obj_to_update = await self.readings_repository.get_by_id(id)
        if not obj_to_update:
            raise EntityNotFoundError(f"Reading with ID {id} not found")

        if role == "user":
            sensor = await self.sensors_repository.get_by_id_and_organization(
                data.sensor_id, organization_id
            )
            if not sensor:
                raise EntityNotFoundError(
                    f"Sensor with ID {data.sensor_id} not found in organization {organization_id}"
                )

        sensor = await self.sensors_repository.get_by_id(data.sensor_id)
        if not sensor:
            raise EntityNotFoundError(f"Sensor with ID {data.sensor_id} not found")

        for field, value in data.model_dump().items():
            setattr(obj_to_update, field, value)
        return await self.readings_repository.update(obj_to_update)

    async def delete(self, id, organization_id: int, role: str):
        obj_to_delete = await self.readings_repository.get_by_id(id)

        if role == "user":
            reading = await self.readings_repository.get_by_id_and_organization(
                id, organization_id
            )
            if not reading:
                raise EntityNotFoundError(
                    f"Reading with ID {id} not found in organization {organization_id}"
                )

        if not obj_to_delete:
            raise EntityNotFoundError(f"Reading with ID {id} not found")
        return await self.readings_repository.delete(id)
