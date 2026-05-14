from sqlalchemy import select

from .. import Session
from ..db_models import Users
from ..interfaces.users_interface import IUsersRepository
from .base_repository import BaseRepository


class UsersRepository(IUsersRepository, BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, Users)

    async def get_user_by_username(self, username: str):
        result = await self.session.execute(
            select(self.model).where(self.model.username == username)
        )
        return result.scalars().first()
