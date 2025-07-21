from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.core.config import settings


engine = create_async_engine(
    str(settings.SQLALCHEMY_DATABASE_URI), echo=True, future=True
)


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def init_db(session: AsyncSession) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines

    # async with engine.begin() as conn:
    #     # await conn.run_sync(SQLModel.metadata.drop_all)
    #     await conn.run_sync(SQLModel.metadata.create_all)
    pass
