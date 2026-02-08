from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def get_by_auth0_sub(
        self, db: AsyncSession, *, auth0_sub: str
    ) -> User | None:
        result = await db.execute(select(User).where(User.auth0_sub == auth0_sub))
        return result.scalars().first()

    async def get_by_email(self, db: AsyncSession, *, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalars().first()


user = CRUDUser(User)
