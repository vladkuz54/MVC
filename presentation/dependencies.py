from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bll.services.alerts_service import AlertsService
from bll.services.devices_service import DevicesService
from bll.services.organizations_service import OrganizationsService
from bll.services.readings_service import ReadingsService
from bll.services.sensors_service import SensorsService
from bll.services.users_service import UsersService
from dal import Session
from dal.repositories.alerts_repository import AlertsRepository
from dal.repositories.devices_repository import DevicesRepository
from dal.repositories.organizations_repository import OrganizationsRepository
from dal.repositories.readings_repository import ReadingsRepository
from dal.repositories.sensors_repository import SensorsRepository
from dal.repositories.users_repository import UsersRepository


async def get_db_session():
    async with Session() as session:
        yield session


def get_organizations_service(
    session: AsyncSession = Depends(get_db_session),
) -> OrganizationsService:
    repository = OrganizationsRepository(session)
    return OrganizationsService(repository)


def get_devices_service(
    session: AsyncSession = Depends(get_db_session),
) -> DevicesService:
    repository = DevicesRepository(session)
    organization_repository = OrganizationsRepository(session)
    return DevicesService(repository, organization_repository)


def get_sensors_service(
    session: AsyncSession = Depends(get_db_session),
) -> SensorsService:
    repository = SensorsRepository(session)
    device_repository = DevicesRepository(session)
    organization_repository = OrganizationsRepository(session)
    return SensorsService(repository, device_repository, organization_repository)


def get_alerts_service(
    session: AsyncSession = Depends(get_db_session),
) -> AlertsService:
    repository = AlertsRepository(session)
    device_repository = DevicesRepository(session)
    organization_repository = OrganizationsRepository(session)
    return AlertsService(repository, device_repository, organization_repository)


def get_readings_service(
    session: AsyncSession = Depends(get_db_session),
) -> ReadingsService:
    repository = ReadingsRepository(session)
    sensor_repository = SensorsRepository(session)
    organization_repository = OrganizationsRepository(session)
    return ReadingsService(repository, sensor_repository, organization_repository)


def get_users_service(
    session: AsyncSession = Depends(get_db_session),
) -> UsersService:
    repository = UsersRepository(session)
    organization_repository = OrganizationsRepository(session)
    return UsersService(repository, organization_repository)
