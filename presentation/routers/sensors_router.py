from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from bll.services.sensors_service import SensorsService

from ..dependencies import get_sensors_service

router = APIRouter(prefix="/sensors", tags=["sensors"])


class SensorRequest(BaseModel):
    device_id: int
    type: str
    unit: str


class SensorResponse(BaseModel):
    id: int
    device_id: int
    type: str
    unit: str
    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[SensorResponse])
async def get_all(service: SensorsService = Depends(get_sensors_service)):
    sensors = await service.get_all()
    return sensors


@router.get("/{id}", response_model=SensorResponse)
async def get_by_id(id: int, service: SensorsService = Depends(get_sensors_service)):
    sensor = await service.get_by_id(id)
    return sensor


@router.post("/", response_model=SensorResponse)
async def create(
    sensor: SensorRequest,
    service: SensorsService = Depends(get_sensors_service),
):
    created = await service.create(sensor)
    return created


@router.put("/{id}", response_model=SensorResponse)
async def update(
    id: int,
    sensor: SensorRequest,
    service: SensorsService = Depends(get_sensors_service),
):
    updated = await service.update(id, sensor)
    return updated


@router.delete("/{id}", response_model=SensorResponse)
async def delete(id: int, service: SensorsService = Depends(get_sensors_service)):
    deleted = await service.delete(id)
    return deleted
