from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict

from bll.services.organizations_service import OrganizationsService

from ..dependencies import get_organizations_service

router = APIRouter(prefix="/organizations", tags=["organizations"])


class OrganizationRequest(BaseModel):
    name: str
    api_key: str


class OrganizationResponse(BaseModel):
    id: int
    name: str
    api_key: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


@router.get("/", response_model=list[OrganizationResponse])
async def get_all(service: OrganizationsService = Depends(get_organizations_service)):
    organizations = await service.get_all()
    return organizations


@router.get("/{id}", response_model=OrganizationResponse)
async def get_by_id(
    id: int, service: OrganizationsService = Depends(get_organizations_service)
):
    organization = await service.get_by_id(id)
    return organization


@router.post("/", response_model=OrganizationResponse)
async def create(
    organization: OrganizationRequest,
    service: OrganizationsService = Depends(get_organizations_service),
):
    created = await service.create(organization)
    return created


@router.put("/{id}", response_model=OrganizationResponse)
async def update(
    id: int,
    organization: OrganizationRequest,
    service: OrganizationsService = Depends(get_organizations_service),
):
    updated = await service.update(id, organization)
    return updated


@router.delete("/{id}", response_model=OrganizationResponse)
async def delete(
    id: int, service: OrganizationsService = Depends(get_organizations_service)
):
    deleted = await service.delete(id)
    return deleted
