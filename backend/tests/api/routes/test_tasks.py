import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.project import project as crud_project
from app.crud.task import task as crud_task
from app.models.user import User
from app.schemas.project import ProjectCreate
from app.schemas.task import TaskCreate


@pytest.mark.asyncio
class TestTaskRoutes:
    async def test_list_tasks_requires_project_id(self, async_client: AsyncClient):
        response = await async_client.get("/api/v1/tasks/")
        assert response.status_code == 400
        assert response.json()["detail"] == "project_id is required"

    async def test_list_tasks_forbidden_for_other_project(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        test_admin_user: User,
    ):
        project = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Admin Project", owner_id=test_admin_user.id),
        )

        response = await async_client.get(f"/api/v1/tasks/?project_id={project.id}")
        assert response.status_code == 403

    async def test_list_tasks_for_own_project(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        test_user: User,
    ):
        project = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="My Project", owner_id=test_user.id),
        )
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(project_id=project.id, title="Task 1"),
        )
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(project_id=project.id, title="Task 2"),
        )

        response = await async_client.get(f"/api/v1/tasks/?project_id={project.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
        assert len(data["items"]) == 2

    async def test_list_tasks_admin_without_project_id(
        self,
        async_client: AsyncClient,
        as_admin: None,
        db_session: AsyncSession,
        test_user: User,
    ):
        project = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Admin List Project", owner_id=test_user.id),
        )
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(project_id=project.id, title="Admin Task"),
        )

        response = await async_client.get("/api/v1/tasks/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1

    async def test_create_task_forbidden(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        test_admin_user: User,
    ):
        project = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Other Project", owner_id=test_admin_user.id),
        )
        payload = {
            "project_id": str(project.id),
            "title": "Forbidden Task",
        }
        response = await async_client.post("/api/v1/tasks/", json=payload)
        assert response.status_code == 403

    async def test_create_task_success(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        test_user: User,
    ):
        project = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="My Task Project", owner_id=test_user.id),
        )
        payload = {
            "project_id": str(project.id),
            "title": "New Task",
            "priority": 4,
        }
        response = await async_client.post("/api/v1/tasks/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["project_id"] == str(project.id)
        assert data["title"] == "New Task"

    async def test_get_task_forbidden(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        test_admin_user: User,
    ):
        project = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Admin Only", owner_id=test_admin_user.id),
        )
        task = await crud_task.create(
            db_session,
            obj_in=TaskCreate(project_id=project.id, title="Hidden Task"),
        )

        response = await async_client.get(f"/api/v1/tasks/{task.id}")
        assert response.status_code == 403

    async def test_update_task(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        test_user: User,
    ):
        project = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Update Task Project", owner_id=test_user.id),
        )
        task = await crud_task.create(
            db_session,
            obj_in=TaskCreate(project_id=project.id, title="Old Title"),
        )

        response = await async_client.patch(
            f"/api/v1/tasks/{task.id}",
            json={"title": "Updated Title"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"

    async def test_delete_task(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        test_user: User,
    ):
        project = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Delete Task Project", owner_id=test_user.id),
        )
        task = await crud_task.create(
            db_session,
            obj_in=TaskCreate(project_id=project.id, title="Delete Me"),
        )

        response = await async_client.delete(f"/api/v1/tasks/{task.id}")
        assert response.status_code == 200

        deleted = await crud_task.get(db_session, id=task.id)
        assert deleted is None
