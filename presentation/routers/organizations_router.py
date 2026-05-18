from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ConfigDict

from bll.services.organizations_service import OrganizationsService

from ..dependencies import get_organizations_service
from .auth import get_current_user

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
async def get_all(
    current_user=Depends(get_current_user),
    service: OrganizationsService = Depends(get_organizations_service),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") == "admin":
        return await service.get_all()
    return await service.get_by_organization(current_user.get("organization_id"))


@router.get("/{id}", response_model=OrganizationResponse)
async def get_by_id(
    id: int,
    current_user=Depends(get_current_user),
    service: OrganizationsService = Depends(get_organizations_service),
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


@router.post("/", response_model=OrganizationResponse)
async def create(
    organization: OrganizationRequest,
    current_user=Depends(get_current_user),
    service: OrganizationsService = Depends(get_organizations_service),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    created = await service.create(organization)
    return created


@router.put("/{id}", response_model=OrganizationResponse)
async def update(
    id: int,
    organization: OrganizationRequest,
    current_user=Depends(get_current_user),
    service: OrganizationsService = Depends(get_organizations_service),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") == "admin":
        updated = await service.update(id, organization)
        return updated
    if current_user.get("organization_id") != id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    updated = await service.update(id, organization)
    return updated


@router.delete("/{id}", response_model=OrganizationResponse)
async def delete(
    id: int,
    current_user=Depends(get_current_user),
    service: OrganizationsService = Depends(get_organizations_service),
):
    if not current_user:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    if current_user.get("role") == "admin":
        deleted = await service.delete(id)
        return deleted
    if current_user.get("organization_id") != id:
        raise HTTPException(
            status_code=403, detail="You are not authorized to perform this action"
        )
    deleted = await service.delete(id)
    return deleted
