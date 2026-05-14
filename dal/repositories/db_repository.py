from sqlalchemy import select
from tqdm import tqdm

from .. import Session
from ..db_models import Alerts, Devices, Organizations, Readings, Sensors
from ..interfaces.db_interfaces import IDBRepository


class DBRepository(IDBRepository):

    def __init__(self, data):
        self.data = data

    async def paste_organizations(self, row):
        async with Session() as session:
            organizations = (
                (
                    await session.execute(
                        select(Organizations).where(
                            Organizations.name == row["organization_name"]
                        )
                    )
                )
                .scalars()
                .first()
            )

            if not organizations:
                organization = Organizations(
                    name=row["organization_name"],
                    api_key=row["organization_api_key"],
                    created_at=row["organization_created_at"],
                )
                session.add(organization)
                await session.commit()

    async def paste_devices(self, row):
        async with Session() as session:
            organizations = (
                (
                    await session.execute(
                        select(Organizations).where(
                            Organizations.name == row["organization_name"]
                        )
                    )
                )
                .scalars()
                .first()
            )

            if organizations:
                devices = (
                    (
                        await session.execute(
                            select(Devices).where(
                                Devices.mac_address == row["device_mac_address"],
                                Devices.organization_id == organizations.id,
                            )
                        )
                    )
                    .scalars()
                    .first()
                )

                if not devices:
                    device = Devices(
                        organization_id=organizations.id,
                        mac_address=row["device_mac_address"],
                        status=row["device_status"],
                        firmware_version=row["device_firmware_version"],
                    )
                    session.add(device)
                    await session.commit()

    async def paste_sensors(self, row):
        async with Session() as session:
            organizations = (
                (
                    await session.execute(
                        select(Organizations).where(
                            Organizations.name == row["organization_name"]
                        )
                    )
                )
                .scalars()
                .first()
            )

            if not organizations:
                return

            devices = (
                (
                    await session.execute(
                        select(Devices).where(
                            Devices.mac_address == row["device_mac_address"],
                            Devices.organization_id == organizations.id,
                        )
                    )
                )
                .scalars()
                .first()
            )

            if not devices:
                return

            sensors = (
                (
                    await session.execute(
                        select(Sensors).where(
                            Sensors.type == row["sensor_type"],
                            Sensors.device_id == devices.id,
                        )
                    )
                )
                .scalars()
                .first()
            )

            if not sensors:
                sensor = Sensors(
                    device_id=devices.id,
                    type=row["sensor_type"],
                    unit=row["sensor_unit"],
                )
                session.add(sensor)
                await session.commit()

    async def paste_readings(self, row):
        async with Session() as session:
            organizations = (
                (
                    await session.execute(
                        select(Organizations).where(
                            Organizations.name == row["organization_name"]
                        )
                    )
                )
                .scalars()
                .first()
            )

            if not organizations:
                return

            devices = (
                (
                    await session.execute(
                        select(Devices).where(
                            Devices.mac_address == row["device_mac_address"],
                            Devices.organization_id == organizations.id,
                        )
                    )
                )
                .scalars()
                .first()
            )

            if not devices:
                return

            sensors = (
                (
                    await session.execute(
                        select(Sensors).where(
                            Sensors.type == row["sensor_type"],
                            Sensors.device_id == devices.id,
                        )
                    )
                )
                .scalars()
                .first()
            )

            if not sensors:
                return

            readings = (
                (
                    await session.execute(
                        select(Readings).where(
                            Readings.timestamp == row["reading_timestamp"],
                            Readings.sensor_id == sensors.id,
                        )
                    )
                )
                .scalars()
                .first()
            )

            if not readings:
                reading = Readings(
                    sensor_id=sensors.id,
                    timestamp=row["reading_timestamp"],
                    value=row["reading_value"],
                )
                session.add(reading)
                await session.commit()

    async def paste_alerts(self, row):
        async with Session() as session:
            organizations = (
                (
                    await session.execute(
                        select(Organizations).where(
                            Organizations.name == row["organization_name"]
                        )
                    )
                )
                .scalars()
                .first()
            )

            if not organizations:
                return

            devices = (
                (
                    await session.execute(
                        select(Devices).where(
                            Devices.mac_address == row["device_mac_address"],
                            Devices.organization_id == organizations.id,
                        )
                    )
                )
                .scalars()
                .first()
            )

            if not devices:
                return

            alerts = (
                (
                    await session.execute(
                        select(Alerts).where(
                            Alerts.message == row["alert_message"],
                            Alerts.device_id == devices.id,
                        )
                    )
                )
                .scalars()
                .first()
            )

            if not alerts:
                alert = Alerts(
                    device_id=devices.id,
                    severity=row["alert_severity"],
                    message=row["alert_message"],
                    is_resolved=row["alert_is_resolved"],
                )
                session.add(alert)
                await session.commit()

    async def paste_all(self):
        for row in tqdm(self.data, desc="Pasting data into the database"):
            await self.paste_organizations(row)
            await self.paste_devices(row)
            await self.paste_sensors(row)
            await self.paste_readings(row)
            await self.paste_alerts(row)
        print("Data has been successfully pasted into the database.")
