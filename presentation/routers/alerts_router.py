from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from bll.services.alerts_service import AlertsService

from ..dependencies import get_alerts_service
from .auth import get_current_user

router = APIRouter(prefix="/alerts", tags=["alerts"])


class AlertRequest(BaseModel):
    device_id: int
    severity: str
    message: str
    is_resolved: bool


class AlertResponse(BaseModel):
    id: int
    device_id: int
    severity: str
    message: str
    is_resolved: bool
    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[AlertResponse])
async def get_all(service: AlertsService = Depends(get_alerts_service)):
    alerts = await service.get_all()
    return alerts


@router.get("/{id}", response_model=AlertResponse)
async def get_by_id(id: int, service: AlertsService = Depends(get_alerts_service)):
    alert = await service.get_by_id(id)
    return alert


@router.post("/", response_model=AlertResponse)
async def create(
    alert: AlertRequest,
    service: AlertsService = Depends(get_alerts_service),
):
    created = await service.create(alert)
    return created


@router.put("/{id}", response_model=AlertResponse)
async def update(
    id: int,
    alert: AlertRequest,
    service: AlertsService = Depends(get_alerts_service),
):
    updated = await service.update(id, alert)
    return updated


@router.delete("/{id}", response_model=AlertResponse)
async def delete(id: int, service: AlertsService = Depends(get_alerts_service)):
    deleted = await service.delete(id)
    return deleted
