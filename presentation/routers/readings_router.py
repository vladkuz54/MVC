from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from bll.services.readings_service import ReadingsService

from ..dependencies import get_readings_service

router = APIRouter(prefix="/readings", tags=["readings"])


class ReadingRequest(BaseModel):
    sensor_id: int
    value: float


class ReadingResponse(BaseModel):
    id: int
    sensor_id: int
    timestamp: datetime
    value: float
    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[ReadingResponse])
async def get_all(service: ReadingsService = Depends(get_readings_service)):
    readings = await service.get_all()
    return readings


@router.get("/between-dates")
async def get_between_dates(
    start: datetime,
    end: datetime,
    limit: int = 100,
    offset: int = 0,
    service: ReadingsService = Depends(get_readings_service),
):
    readings = await service.get_between_dates(start, end, limit, offset)
    return [r for r in readings]


@router.get("/{id}", response_model=ReadingResponse)
async def get_by_id(id: int, service: ReadingsService = Depends(get_readings_service)):
    reading = await service.get_by_id(id)
    return reading


@router.post("/", response_model=ReadingResponse)
async def create(
    reading: ReadingRequest,
    service: ReadingsService = Depends(get_readings_service),
):
    created = await service.create(reading)
    return created


@router.put("/{id}", response_model=ReadingResponse)
async def update(
    id: int,
    reading: ReadingRequest,
    service: ReadingsService = Depends(get_readings_service),
):
    updated = await service.update(id, reading)
    return updated


@router.delete("/{id}", response_model=ReadingResponse)
async def delete(id: int, service: ReadingsService = Depends(get_readings_service)):
    deleted = await service.delete(id)
    return deleted
