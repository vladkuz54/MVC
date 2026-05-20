from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from bll.services.sensors_service import SensorsService

from ..dependencies import get_sensors_service
from .auth import get_current_user

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
async def get_all(
    current_user=Depends(get_current_user),
    service: SensorsService = Depends(get_sensors_service),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") == "admin":
        return await service.get_all()
    return await service.get_by_organization(current_user.get("organization_id"))


@router.get("/{id}", response_model=SensorResponse)
async def get_by_id(
    id: int,
    service: SensorsService = Depends(get_sensors_service),
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") == "admin":
        return await service.get_by_id(id)
    return await service.get_by_id_and_organization(
        id, current_user.get("organization_id")
    )


@router.post("/", response_model=SensorResponse)
async def create(
    sensor: SensorRequest,
    service: SensorsService = Depends(get_sensors_service),
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    created = await service.create(
        sensor, current_user.get("organization_id"), current_user.get("role")
    )
    return created


@router.put("/{id}", response_model=SensorResponse)
async def update(
    id: int,
    sensor: SensorRequest,
    current_user=Depends(get_current_user),
    service: SensorsService = Depends(get_sensors_service),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    updated = await service.update(
        id, sensor, current_user.get("organization_id"), current_user.get("role")
    )
    return updated


@router.delete("/{id}", response_model=SensorResponse)
async def delete(
    id: int,
    service: SensorsService = Depends(get_sensors_service),
    current_user=Depends(get_current_user),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    deleted = await service.delete(
        id, current_user.get("organization_id"), current_user.get("role")
    )
    return deleted
