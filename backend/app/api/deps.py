from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from fastapi_plugin import Auth0FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import async_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session.begin() as session:
        yield session


DBDep = Annotated[AsyncSession, Depends(get_db)]


auth0 = Auth0FastAPI(
    domain=settings.AUTH0_DOMAIN,
    audience=settings.AUTH0_AUDIENCE,
)
