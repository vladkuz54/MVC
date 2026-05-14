from pydantic import BaseModel

from dal.db_models import Users
from dal.interfaces.organizations_interfaces import IOrganizationsRepository
from dal.interfaces.users_interface import IUsersRepository

from ..exceptions import EntityNotFoundError
from ..interfaces.users_interface import IUsersService


class UserRequest(BaseModel):
    username: str
    password: str
    role: str
    organization_id: int


class UsersService(IUsersService):

    def __init__(
        self,
        repository: IUsersRepository,
        organizations_repository: IOrganizationsRepository,
    ):
        self.repository = repository
        self.organizations_repository = organizations_repository

    async def get_user_by_username(self, username: str):
        obj_to_get = await self.repository.get_user_by_username(username)
        if not obj_to_get:
            raise EntityNotFoundError(f"User with username {username} not found")
        return await self.repository.get_user_by_username(username)

    async def create(self, data: UserRequest):
        organization = await self.organizations_repository.get_by_id(
            data.organization_id
        )
        if not organization:
            raise EntityNotFoundError(
                f"Organization with ID {data.organization_id} not found"
            )

        obj_to_create = Users(
            username=data.username,
            hashed_password=data.password,
            role=data.role,
            organization_id=data.organization_id,
        )
        return await self.repository.create(obj_to_create)
