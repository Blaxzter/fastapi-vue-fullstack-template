"""Project fixtures for testing."""

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.user import User


@pytest_asyncio.fixture
async def test_project(db_session: AsyncSession, test_user: User) -> Project:
    """Create a test project."""
    project = Project(
        name="Test Project",
        description="A test project",
        status="active",
        owner_id=test_user.id,
    )
    db_session.add(project)
    await db_session.flush()
    await db_session.refresh(project)
    return project


@pytest_asyncio.fixture
async def test_project_without_owner(db_session: AsyncSession) -> Project:
    """Create a test project without an owner."""
    project = Project(
        name="Orphan Project",
        description="A project without an owner",
        status="active",
        owner_id=None,
    )
    db_session.add(project)
    await db_session.flush()
    await db_session.refresh(project)
    return project
