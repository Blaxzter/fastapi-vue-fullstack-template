"""Task fixtures for testing."""

from datetime import date

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.models.task import Task


@pytest_asyncio.fixture
async def test_task(db_session: AsyncSession, test_project: Project) -> Task:
    """Create a test task."""
    task = Task(
        project_id=test_project.id,
        title="Test Task",
        description="A test task",
        status="todo",
        priority=3,
        due_date=date(2026, 12, 31),
    )
    db_session.add(task)
    await db_session.flush()
    await db_session.refresh(task)
    return task


@pytest_asyncio.fixture
async def multiple_test_tasks(
    db_session: AsyncSession, test_project: Project
) -> list[Task]:
    """Create multiple test tasks."""
    tasks = [
        Task(
            project_id=test_project.id,
            title=f"Task {i}",
            description=f"Description {i}",
            status="todo" if i % 2 == 0 else "in_progress",
            priority=i % 5 + 1,
            due_date=date(2026, 12, i + 1),
        )
        for i in range(5)
    ]
    for task in tasks:
        db_session.add(task)
    await db_session.flush()
    for task in tasks:
        await db_session.refresh(task)
    return tasks
