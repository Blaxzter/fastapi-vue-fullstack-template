import uuid
from typing import Any, Literal

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser, DBDep
from app.crud.project import project as crud_project
from app.crud.task import task as crud_task
from app.schemas.task import TaskCreate, TaskListResponse, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

TaskSortField = Literal[
    "title", "status", "priority", "due_date", "created_at", "updated_at"
]
SortDirection = Literal["asc", "desc"]


async def _get_project_for_access(
    session: AsyncSession,
    project_id: uuid.UUID,
    current_user: CurrentUser,
):
    project = await crud_project.get(session, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    if not current_user.is_admin and project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return project


@router.get("/", response_model=TaskListResponse)
async def list_tasks(
    session: DBDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 50,
    search: str | None = None,
    status: str | None = None,
    project_id: uuid.UUID | None = None,
    sort_by: TaskSortField = "created_at",
    sort_dir: SortDirection = "desc",
) -> Any:
    if not current_user.is_admin:
        if not project_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="project_id is required",
            )
        await _get_project_for_access(session, project_id, current_user)

    items = await crud_task.get_multi_filtered(
        session,
        skip=skip,
        limit=limit,
        search=search,
        status=status,
        project_id=project_id,
        sort_by=sort_by,
        sort_dir=sort_dir,
    )
    total = await crud_task.get_count_filtered(
        session,
        search=search,
        status=status,
        project_id=project_id,
    )
    return TaskListResponse(items=items, total=total, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: uuid.UUID,
    session: DBDep,
    current_user: CurrentUser,
) -> Any:
    task = await crud_task.get(session, id=task_id, raise_404_error=True)
    await _get_project_for_access(session, task.project_id, current_user)
    return task


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    session: DBDep,
    current_user: CurrentUser,
) -> Any:
    await _get_project_for_access(session, task_in.project_id, current_user)
    return await crud_task.create(session, obj_in=task_in)


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: uuid.UUID,
    task_in: TaskUpdate,
    session: DBDep,
    current_user: CurrentUser,
) -> Any:
    task = await crud_task.get(session, id=task_id, raise_404_error=True)
    await _get_project_for_access(session, task.project_id, current_user)
    if task_in.project_id:
        await _get_project_for_access(session, task_in.project_id, current_user)
    return await crud_task.update(session, db_obj=task, obj_in=task_in)


@router.delete("/{task_id}", response_model=TaskRead)
async def delete_task(
    task_id: uuid.UUID,
    session: DBDep,
    current_user: CurrentUser,
) -> Any:
    task = await crud_task.get(session, id=task_id, raise_404_error=True)
    await _get_project_for_access(session, task.project_id, current_user)
    await session.delete(task)
    await session.commit()
    return task
