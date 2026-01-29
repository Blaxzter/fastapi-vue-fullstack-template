from collections.abc import AsyncGenerator, Iterable
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi_plugin import Auth0FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import async_session
from app.crud.user import user as crud_user
from app.models.user import User
from app.schemas.user import UserCreate


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session.begin() as session:
        yield session


DBDep = Annotated[AsyncSession, Depends(get_db)]


auth0 = Auth0FastAPI(
    domain=settings.AUTH0_DOMAIN,
    audience=settings.AUTH0_AUDIENCE,
)


def _normalize_required_roles(
    required_roles: str | Iterable[str] | None,
) -> list[str]:
    if required_roles is None:
        return []
    if isinstance(required_roles, str):
        return [required_roles]
    return list(required_roles)


async def _get_or_create_user(
    session: AsyncSession,
    claims: dict,
) -> User:
    auth0_sub = claims.get("sub")
    if not auth0_sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication payload",
        )

    user = await crud_user.get_by_auth0_sub(session, auth0_sub=auth0_sub)
    if user:
        return user

    user_in = UserCreate(
        auth0_sub=auth0_sub,
        email=claims.get("email"),
        name=claims.get("name") or claims.get("nickname"),
    )
    return await crud_user.create(session, obj_in=user_in)


def current_user(required_roles: str | Iterable[str] | None = None):
    required_roles_list = _normalize_required_roles(required_roles)

    async def _current_user(
        session: DBDep,
        claims: dict = Depends(auth0.require_auth()),
    ) -> User:
        user = await _get_or_create_user(session, claims)

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        if required_roles_list and not set(required_roles_list).issubset(
            set(user.roles)
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        return user

    return _current_user


CurrentUser = Annotated[User, Depends(current_user())]
CurrentSuperuser = Annotated[User, Depends(current_user("admin"))]
