import uuid
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import delete

from app.api.deps import CurrentSuperuser, CurrentUser, DBDep
from app.crud.project import project as crud_project
from app.models.task import Task
from app.schemas.project import (
    ProjectCreate,
    ProjectListResponse,
    ProjectRead,
    ProjectUpdate,
)

router = APIRouter(prefix="/projects", tags=["projects"])

ProjectSortField = Literal["name", "status", "created_at", "updated_at"]
SortDirection = Literal["asc", "desc"]


def _ensure_project_access(
    project_owner_id: uuid.UUID | None,
    current_user: CurrentUser,
) -> None:
    if current_user.is_admin:
        return
    if not project_owner_id or project_owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )


@router.get("/", response_model=ProjectListResponse)
async def list_projects(
    session: DBDep,
    _: CurrentSuperuser,
    skip: int = 0,
    limit: int = 50,
    search: str | None = None,
    status: str | None = None,
    owner_id: uuid.UUID | None = None,
    sort_by: ProjectSortField = "created_at",
    sort_dir: SortDirection = "desc",
) -> Any:
    items = await crud_project.get_multi_filtered(
        session,
        skip=skip,
        limit=limit,
        search=search,
        status=status,
        owner_id=owner_id,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )
    total = await crud_project.get_count_filtered(
        session,
        search=search,
        status=status,
        owner_id=owner_id,
    )
    return ProjectListResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/me", response_model=ProjectListResponse)
async def list_my_projects(
    session: DBDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 50,
    search: str | None = None,
    status: str | None = None,
    sort_by: ProjectSortField = "created_at",
    sort_dir: SortDirection = "desc",
) -> Any:
    items = await crud_project.get_multi_filtered(
        session,
        skip=skip,
        limit=limit,
        search=search,
        status=status,
        owner_id=current_user.id,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )
    total = await crud_project.get_count_filtered(
        session,
        search=search,
        status=status,
        owner_id=current_user.id,
    )
    return ProjectListResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: uuid.UUID,
    session: DBDep,
    current_user: CurrentUser,
) -> Any:
    project = await crud_project.get(session, id=project_id, raise_404_error=True)
    _ensure_project_access(project.owner_id, current_user)
    return project


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_in: ProjectCreate,
    session: DBDep,
    current_user: CurrentUser,
) -> Any:
    project_data = project_in.model_dump()
    if not current_user.is_admin:
        project_data["owner_id"] = current_user.id
    elif project_data.get("owner_id") is None:
        project_data["owner_id"] = current_user.id
    return await crud_project.create(session, obj_in=ProjectCreate(**project_data))


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: uuid.UUID,
    project_in: ProjectUpdate,
    session: DBDep,
    current_user: CurrentUser,
) -> Any:
    project = await crud_project.get(session, id=project_id, raise_404_error=True)
    _ensure_project_access(project.owner_id, current_user)
    if not current_user.is_admin and project_in.owner_id is not None:
        project_in.owner_id = None
    return await crud_project.update(session, db_obj=project, obj_in=project_in)


@router.delete("/{project_id}", response_model=ProjectRead)
async def delete_project(
    project_id: uuid.UUID,
    session: DBDep,
    current_user: CurrentUser,
) -> Any:
    project = await crud_project.get(session, id=project_id, raise_404_error=True)
    _ensure_project_access(project.owner_id, current_user)
    await session.execute(delete(Task).where(Task.project_id == project_id))
    await session.delete(project)
    await session.commit()
    return project
