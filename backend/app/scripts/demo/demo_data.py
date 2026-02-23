import logging
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.task import Task
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_demo_data(
    session: AsyncSession, owner_id: uuid.UUID | None = None
) -> None:
    if owner_id is not None:
        # Seed per-user: check if this user already has projects
        existing = await session.execute(
            select(Project).where(Project.owner_id == owner_id)
        )
        if existing.scalars().first():
            logger.info("Demo data already exists for user %s, skipping seed", owner_id)
            return
    else:
        # Legacy: seed globally using first user
        existing = await session.execute(select(Project))
        if existing.scalars().first():
            logger.info("Demo data already exists, skipping seed")
            return
        result = await session.execute(select(User))
        first_user = result.scalars().first()
        owner_id = first_user.id if first_user else None

    projects = [
        Project(
            name="Acme Onboarding",
            description="Launch checklist for new hires and tools access",
            status="active",
            owner_id=owner_id,
        ),
        Project(
            name="Marketing Website",
            description="Public-facing site refresh and SEO improvements",
            status="active",
            owner_id=owner_id,
        ),
        Project(
            name="Internal Tools",
            description="Admin dashboard for ops and support workflows",
            status="archived",
            owner_id=owner_id,
        ),
    ]
    session.add_all(projects)
    await session.flush()

    tasks = [
        Task(
            project_id=projects[0].id,
            title="Create onboarding checklist",
            description="Document accounts, permissions, and key links",
            status="todo",
            priority=2,
        ),
        Task(
            project_id=projects[0].id,
            title="Schedule intro sessions",
            description="Meet with engineering, product, and design",
            status="in_progress",
            priority=3,
        ),
        Task(
            project_id=projects[1].id,
            title="Audit existing pages",
            description="Inventory top pages and current traffic",
            status="done",
            priority=4,
        ),
        Task(
            project_id=projects[1].id,
            title="Prepare new hero copy",
            description="Draft updated value props and CTA",
            status="todo",
            priority=3,
        ),
        Task(
            project_id=projects[2].id,
            title="Collect admin feedback",
            description="Interview support and ops for pain points",
            status="done",
            priority=2,
        ),
    ]
    session.add_all(tasks)

    logger.info("Seeded demo projects and tasks")
