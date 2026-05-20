from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from bll.services.readings_service import ReadingsService

from ..dependencies import get_readings_service
from .auth import get_current_user

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
async def get_all(
    service: ReadingsService = Depends(get_readings_service),
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") == "admin":
        return await service.get_all()
    return await service.get_by_organization(current_user.get("organization_id"))


@router.get("/{id}", response_model=ReadingResponse)
async def get_by_id(
    id: int,
    service: ReadingsService = Depends(get_readings_service),
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") == "admin":
        return await service.get_by_id(id)
    return await service.get_by_id_and_organization(
        id, current_user.get("organization_id")
    )


@router.post("/", response_model=ReadingResponse)
async def create(
    reading: ReadingRequest,
    service: ReadingsService = Depends(get_readings_service),
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )
    created = await service.create(reading, current_user.get("organization_id"), current_user.get("role"))
    return created


@router.put("/{id}", response_model=ReadingResponse)
async def update(
    id: int,
    reading: ReadingRequest,
    service: ReadingsService = Depends(get_readings_service),
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )
    updated = await service.update(id, reading, current_user.get("organization_id"), current_user.get("role"))
    return updated


@router.delete("/{id}", response_model=ReadingResponse)
async def delete(
    id: int,
    service: ReadingsService = Depends(get_readings_service),
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=401, detail="You are not authorized to perform this action"
        )
    deleted = await service.delete(id, current_user.get("organization_id"), current_user.get("role"))
    return deleted
