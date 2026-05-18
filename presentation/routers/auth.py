import datetime
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from bll.services.users_service import UsersService

from ..dependencies import get_users_service

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY = "jewofjwdifnvjidvnjidedevde"
ALGORITHM = "HS256"

bcrypth_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class UserRequest(BaseModel):
    username: str
    password: str
    role: str
    organization_id: int


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


async def authicate_user(
    username: str,
    password: str,
    service: UsersService,
):
    user = await service.get_user_by_username(username)
    if not user or not bcrypth_context.verify(password, user.hashed_password):
        return None

    return user


async def create_access_token(
    username: str,
    user_id: int,
    organization_id: int,
    role: str,
    expires_delta: timedelta,
):
    encode = {
        "sub": username,
        "user_id": user_id,
        "organization_id": organization_id,
        "role": role,
    }

    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        user_role: str = payload.get("role")
        organization_id: int = payload.get("organization_id")

        if not username or not user_id or not user_role or not organization_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        return {
            "username": username,
            "user_id": user_id,
            "organization_id": organization_id,
            "role": user_role,
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.post("/")
async def create_user(
    user: UserRequest, service: UsersService = Depends(get_users_service)
):
    user.password = bcrypth_context.hash(user.password)
    created = await service.create(user)
    return created


@router.post("/token", response_model=TokenResponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UsersService = Depends(get_users_service),
):
    user = await authicate_user(
        form_data.username,
        form_data.password,
        service,
    )
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = await create_access_token(
        user.username, user.id, user.organization_id, user.role, timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
