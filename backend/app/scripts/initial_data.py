import asyncio
import logging

from app.core.db import async_session, init_db
from app.scripts.demo.demo_data import seed_demo_data

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    async with async_session.begin() as session:
        await init_db(session)
        await seed_demo_data(session)


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
