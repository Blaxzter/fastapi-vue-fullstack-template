import uuid
from typing import Literal

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

TaskSortField = Literal[
    "title", "status", "priority", "due_date", "created_at", "updated_at"
]
SortDirection = Literal["asc", "desc"]


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    async def get_multi_filtered(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        search: str | None = None,
        status: str | None = None,
        project_id: uuid.UUID | None = None,
        sort_by: TaskSortField = "created_at",
        sort_dir: SortDirection = "desc",
    ) -> list[Task]:
        query = select(Task)

        if search:
            like = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Task.title.ilike(like),
                    Task.description.ilike(like),
                )
            )

        if status:
            query = query.where(Task.status == status)

        if project_id:
            query = query.where(Task.project_id == project_id)

        sort_column = {
            "title": Task.title,
            "status": Task.status,
            "priority": Task.priority,
            "due_date": Task.due_date,
            "created_at": Task.created_at,
            "updated_at": Task.updated_at,
        }.get(sort_by, Task.created_at)

        if sort_dir == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_count_filtered(
        self,
        db: AsyncSession,
        *,
        search: str | None = None,
        status: str | None = None,
        project_id: uuid.UUID | None = None,
    ) -> int:
        query = select(func.count()).select_from(Task)

        if search:
            like = f"%{search.strip()}%"
            query = query.where(
                or_(
                    Task.title.ilike(like),
                    Task.description.ilike(like),
                )
            )

        if status:
            query = query.where(Task.status == status)

        if project_id:
            query = query.where(Task.project_id == project_id)

        result = await db.execute(query)
        return result.scalar() or 0


task = CRUDTask(Task)
