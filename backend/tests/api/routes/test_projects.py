import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.project import project as crud_project
from app.models.user import User
from app.schemas.project import ProjectCreate


@pytest.mark.asyncio
class TestProjectRoutes:
    async def test_list_projects(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        test_user: User,
    ):
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(
                name="List Project",
                description="List project",
                owner_id=test_user.id,
            ),
        )
        response = await async_client.get("/api/v1/projects/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] >= 1
        assert data["items"]

    async def test_list_my_projects(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        test_user: User,
    ):
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Mine", owner_id=test_user.id),
        )
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Not Mine", owner_id=None),
        )

        response = await async_client.get("/api/v1/projects/me")
        assert response.status_code == 200
        data = response.json()
        assert all(item["owner_id"] == str(test_user.id) for item in data["items"])

    async def test_create_project_sets_owner(
        self,
        async_client: AsyncClient,
        test_user: User,
        test_admin_user: User,
    ):
        payload = {
            "name": "Created Project",
            "description": "From API",
            "status": "active",
            "owner_id": str(test_admin_user.id),
        }
        response = await async_client.post("/api/v1/projects/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Created Project"
        assert data["owner_id"] == str(test_user.id)

    async def test_get_project_forbidden(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        test_admin_user: User,
    ):
        project = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Admin Project", owner_id=test_admin_user.id),
        )

        response = await async_client.get(f"/api/v1/projects/{project.id}")
        assert response.status_code == 403

    async def test_update_project(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        test_user: User,
    ):
        project = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Update Me", owner_id=test_user.id),
        )

        response = await async_client.patch(
            f"/api/v1/projects/{project.id}",
            json={"name": "Updated Project"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(project.id)
        assert data["name"] == "Updated Project"

    async def test_delete_project(
        self,
        async_client: AsyncClient,
        db_session: AsyncSession,
        test_user: User,
    ):
        project = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Delete Me", owner_id=test_user.id),
        )

        response = await async_client.delete(f"/api/v1/projects/{project.id}")
        assert response.status_code == 200

        deleted = await crud_project.get(db_session, id=project.id)
        assert deleted is None
