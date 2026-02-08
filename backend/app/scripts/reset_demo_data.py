import asyncio
import logging

from sqlalchemy import delete

from app.core.db import async_session
from app.models.project import Project
from app.models.task import Task
from app.scripts.initial_data import seed_demo_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def reset_demo_data() -> None:
    async with async_session.begin() as session:
        await session.execute(delete(Task))
        await session.execute(delete(Project))
    logger.info("Cleared demo projects and tasks")


async def main() -> None:
    await reset_demo_data()
    await seed_demo_data()
    logger.info("Reset demo data complete")


if __name__ == "__main__":
    asyncio.run(main())
