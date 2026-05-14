from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from . import Base, engine
from .interfaces.db_interfaces import IDBModels


class Organizations(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    api_key = Column(String, index=True)
    created_at = Column(Date, nullable=False, default=datetime.now())

    devices = relationship(
        "Devices", back_populates="organization", cascade="all, delete-orphan"
    )

    users = relationship(
        "Users", back_populates="organization", cascade="all, delete-orphan"
    )


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum("admin", "user", name="user_roles"), default="user")
    organization_id = Column(Integer, ForeignKey("organizations.id"))

    organization = relationship("Organizations", back_populates="users")


class Devices(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    mac_address = Column(String, index=True)
    status = Column(Boolean, default=True)
    firmware_version = Column(String, nullable=True)

    organization = relationship("Organizations", back_populates="devices")
    sensors = relationship(
        "Sensors", back_populates="device", cascade="all, delete-orphan"
    )
    alerts = relationship(
        "Alerts", back_populates="device", cascade="all, delete-orphan"
    )


class Alerts(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    severity = Column(String, nullable=False)
    message = Column(String, nullable=False)
    is_resolved = Column(Boolean, default=False)

    device = relationship("Devices", back_populates="alerts")


class Sensors(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    type = Column(String, nullable=False)
    unit = Column(String, nullable=False)

    device = relationship("Devices", back_populates="sensors")
    readings = relationship(
        "Readings", back_populates="sensor", cascade="all, delete-orphan"
    )


class Readings(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    timestamp = Column(DateTime, nullable=False, default=datetime.now())
    value = Column(Float, nullable=False)

    sensor = relationship("Sensors", back_populates="readings")


class DBModels(IDBModels):
    async def init_db(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_db(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
