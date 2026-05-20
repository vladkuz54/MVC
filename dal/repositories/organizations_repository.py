from sqlalchemy import select

from .. import Session
from ..db_models import Organizations
from ..interfaces.organizations_interfaces import IOrganizationsRepository
from .base_repository import BaseRepository


class OrganizationsRepository(BaseRepository, IOrganizationsRepository):
    def __init__(self, session: Session):
        super().__init__(session, Organizations)

    async def get_by_organization(self, organization_id):
        result = await self.session.execute(
            select(self.model).where(self.model.id == organization_id)
        )
        return result.scalars()
