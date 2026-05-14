from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict

from .auth import get_current_user
from bll.services.users_service import UsersService

from ..dependencies import get_users_service



class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    organization_id: int
    model_config = ConfigDict(from_attributes=True)

router = APIRouter(prefix="/users", tags=["users"])
bcrypth_context = CryptContext(schemes=["bcrypt"], deprecated="auto")   

@router.get("/", response_model=UserResponse)
async def get_user_info(current_user: Annotated[dict, Depends(get_current_user)], service: UsersService = Depends(get_users_service)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    return await service.get_by_id(current_user["id"])

