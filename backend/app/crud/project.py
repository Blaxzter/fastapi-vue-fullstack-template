import uuid
from collections.abc import Sequence
from typing import Literal

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

ProjectSortField = Literal["name", "status", "created_at", "updated_at"]
SortDirection = Literal["asc", "desc"]


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    async def get_multi_filtered(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        search: str | None = None,
        status: str | None = None,
        owner_id: uuid.UUID | None = None,
        sort_by: ProjectSortField = "created_at",
        sort_dir: SortDirection = "desc",
    ) -> Sequence[Project]:
        query = select(Project)

        if search:
            like = f"%{search.strip()}%"
            query = query.where(
                or_(
                    col(Project.name).ilike(like),
                    col(Project.description).ilike(like),
                )
            )

        if status:
            query = query.where(col(Project.status) == status)

        if owner_id:
            query = query.where(col(Project.owner_id) == owner_id)

        sort_column = {
            "name": col(Project.name),
            "status": col(Project.status),
            "created_at": col(Project.created_at),
            "updated_at": col(Project.updated_at),
        }.get(sort_by, col(Project.created_at))

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
        owner_id: uuid.UUID | None = None,
    ) -> int:
        query = select(func.count()).select_from(Project)

        if search:
            like = f"%{search.strip()}%"
            query = query.where(
                or_(
                    col(Project.name).ilike(like),
                    col(Project.description).ilike(like),
                )
            )

        if status:
            query = query.where(col(Project.status) == status)

        if owner_id:
            query = query.where(col(Project.owner_id) == owner_id)

        result = await db.execute(query)
        return result.scalar() or 0


project = CRUDProject(Project)
