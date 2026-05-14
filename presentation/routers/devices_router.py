from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from bll.services.devices_service import DevicesService

from ..dependencies import get_devices_service

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
async def get_all(service: DevicesService = Depends(get_devices_service)):
    devices = await service.get_all()
    return devices


@router.get("/{id}", response_model=DeviceResponse)
async def get_by_id(id: int, service: DevicesService = Depends(get_devices_service)):
    device = await service.get_by_id(id)
    return device


@router.post("/", response_model=DeviceResponse)
async def create(
    device: DeviceRequest,
    service: DevicesService = Depends(get_devices_service),
):
    created = await service.create(device)
    return created


@router.put("/{id}", response_model=DeviceResponse)
async def update(
    id: int,
    device: DeviceRequest,
    service: DevicesService = Depends(get_devices_service),
):
    updated = await service.update(id, device)
    return updated


@router.delete("/{id}", response_model=DeviceResponse)
async def delete(id: int, service: DevicesService = Depends(get_devices_service)):
    deleted = await service.delete(id)
    return deleted
