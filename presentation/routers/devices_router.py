from fastapi import HTTPException
from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from bll.services.devices_service import DevicesService

from ..dependencies import get_devices_service
from .auth import get_current_user

router = APIRouter(prefix="/devices", tags=["devices"])


class DeviceRequest(BaseModel):
    organization_id: int
    mac_address: str
    status: bool
    firmware_version: str


class DeviceResponse(BaseModel):
    id: int
    organization_id: int
    mac_address: str
    status: bool
    firmware_version: str
    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[DeviceResponse])
async def get_all(
    current_user=Depends(get_current_user),
    service: DevicesService = Depends(get_devices_service),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") == "admin":
        return await service.get_all()
    return await service.get_by_organization(current_user.get("organization_id"))


@router.get("/{id}", response_model=DeviceResponse)
async def get_by_id(
    id: int,
    current_user=Depends(get_current_user),
    service: DevicesService = Depends(get_devices_service),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") == "admin":
        return await service.get_by_id(id)
    if current_user.get("organization_id") != id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    return await service.get_by_id(id)


@router.post("/", response_model=DeviceResponse)
async def create(
    device: DeviceRequest,
    current_user=Depends(get_current_user),
    service: DevicesService = Depends(get_devices_service),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") == "admin":
        return await service.create(device)
    if device.organization_id != current_user.get("organization_id"):
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    return await service.create(device)


@router.put("/{id}", response_model=DeviceResponse)
async def update(
    id: int,
    device: DeviceRequest,
    current_user=Depends(get_current_user),
    service: DevicesService = Depends(get_devices_service),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") == "admin":
        return await service.update(id, device)
    if current_user.get("organization_id") != id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    if device.organization_id != current_user.get("organization_id"):
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    return await service.update(id, device)


@router.delete("/{id}", response_model=DeviceResponse)
async def delete(
    id: int,
    current_user=Depends(get_current_user),
    service: DevicesService = Depends(get_devices_service),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") == "admin":
        return await service.delete(id)
    if current_user.get("organization_id") != id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    return await service.delete(id)
