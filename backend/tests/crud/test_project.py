"""Unit tests for Project CRUD operations."""

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.project import project as crud_project
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate


@pytest.mark.asyncio
class TestProjectCRUD:
    """Test suite for Project CRUD operations."""

    async def test_create_project(self, db_session: AsyncSession, test_user: User):
        """Test creating a new project."""
        project_in = ProjectCreate(
            name="New Project",
            description="A brand new project",
            status="active",
            owner_id=test_user.id,
        )
        project = await crud_project.create(db_session, obj_in=project_in)

        assert project.name == "New Project"
        assert project.description == "A brand new project"
        assert project.status == "active"
        assert project.owner_id == test_user.id
        assert project.id is not None

    async def test_create_project_without_owner(self, db_session: AsyncSession):
        """Test creating a project without an owner."""
        project_in = ProjectCreate(
            name="Orphan Project",
            description="No owner",
            status="active",
            owner_id=None,
        )
        project = await crud_project.create(db_session, obj_in=project_in)

        assert project.name == "Orphan Project"
        assert project.owner_id is None

    async def test_get_project(self, db_session: AsyncSession, test_project: Project):
        """Test getting a project by ID."""
        project = await crud_project.get(db_session, id=test_project.id)

        assert project is not None
        assert project.id == test_project.id
        assert project.name == test_project.name

    async def test_get_project_not_found(self, db_session: AsyncSession):
        """Test getting a non-existent project."""
        import uuid

        fake_id = uuid.uuid4()
        project = await crud_project.get(db_session, id=fake_id)

        assert project is None

    async def test_get_project_not_found_with_error(self, db_session: AsyncSession):
        """Test getting a non-existent project with raise_404_error=True."""
        import uuid

        fake_id = uuid.uuid4()
        with pytest.raises(HTTPException) as exc_info:
            await crud_project.get(db_session, id=fake_id, raise_404_error=True)

        assert exc_info.value.status_code == 404
        assert "Project not found" in str(exc_info.value.detail)

    async def test_get_multi_projects(
        self, db_session: AsyncSession, test_project: Project
    ):
        """Test getting multiple projects."""
        # Create additional projects
        for i in range(3):
            project_in = ProjectCreate(
                name=f"Project {i}",
                description=f"Description {i}",
                status="active",
            )
            await crud_project.create(db_session, obj_in=project_in)

        projects = await crud_project.get_multi(db_session, skip=0, limit=10)

        assert len(projects) == 4  # 1 from fixture + 3 created

    async def test_update_project(
        self, db_session: AsyncSession, test_project: Project
    ):
        """Test updating a project."""
        project_update = ProjectUpdate(
            name="Updated Project",
            description="Updated description",
        )
        updated_project = await crud_project.update(
            db_session, db_obj=test_project, obj_in=project_update
        )

        assert updated_project.id == test_project.id
        assert updated_project.name == "Updated Project"
        assert updated_project.description == "Updated description"

    async def test_update_project_status(
        self, db_session: AsyncSession, test_project: Project
    ):
        """Test updating project status."""
        project_update = ProjectUpdate(status="archived")
        updated_project = await crud_project.update(
            db_session, db_obj=test_project, obj_in=project_update
        )

        assert updated_project.status == "archived"

    async def test_remove_project(
        self, db_session: AsyncSession, test_project: Project
    ):
        """Test removing a project."""
        project_id = test_project.id
        removed_project = await crud_project.remove(db_session, id=project_id)

        assert removed_project is not None
        assert removed_project.id == project_id

        # Verify project is deleted
        project = await crud_project.get(db_session, id=project_id)
        assert project is None

    async def test_get_multi_filtered_by_search(
        self, db_session: AsyncSession, test_user: User
    ):
        """Test filtering projects by search query."""
        # Create projects with specific names
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(
                name="Alpha Project", description="Search test", owner_id=test_user.id
            ),
        )
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(
                name="Beta Project", description="Another test", owner_id=test_user.id
            ),
        )
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(
                name="Gamma Task", description="Different", owner_id=test_user.id
            ),
        )

        # Search for "Project" in name
        projects = await crud_project.get_multi_filtered(
            db_session, search="Project", skip=0, limit=10
        )

        assert len(projects) == 2
        project_names = [p.name for p in projects]
        assert "Alpha Project" in project_names
        assert "Beta Project" in project_names
        assert "Gamma Task" not in project_names

    async def test_get_multi_filtered_by_status(
        self, db_session: AsyncSession, test_user: User
    ):
        """Test filtering projects by status."""
        # Create projects with different statuses
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(
                name="Active 1", status="active", owner_id=test_user.id
            ),
        )
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(
                name="Active 2", status="active", owner_id=test_user.id
            ),
        )
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(
                name="Archived 1", status="archived", owner_id=test_user.id
            ),
        )

        # Filter by active status
        active_projects = await crud_project.get_multi_filtered(
            db_session, status="active", skip=0, limit=10
        )

        assert len(active_projects) == 2
        assert all(p.status == "active" for p in active_projects)

        # Filter by archived status
        archived_projects = await crud_project.get_multi_filtered(
            db_session, status="archived", skip=0, limit=10
        )

        assert len(archived_projects) == 1
        assert archived_projects[0].status == "archived"

    async def test_get_multi_filtered_by_owner(
        self, db_session: AsyncSession, test_user: User, test_admin_user: User
    ):
        """Test filtering projects by owner."""
        # Create projects for different users
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="User Project", owner_id=test_user.id),
        )
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Admin Project", owner_id=test_admin_user.id),
        )

        # Filter by test_user
        user_projects = await crud_project.get_multi_filtered(
            db_session, owner_id=test_user.id, skip=0, limit=10
        )

        assert len(user_projects) == 1
        assert user_projects[0].owner_id == test_user.id

        # Filter by test_admin_user
        admin_projects = await crud_project.get_multi_filtered(
            db_session, owner_id=test_admin_user.id, skip=0, limit=10
        )

        assert len(admin_projects) == 1
        assert admin_projects[0].owner_id == test_admin_user.id

    async def test_get_multi_filtered_with_sorting(
        self, db_session: AsyncSession, test_user: User
    ):
        """Test sorting projects."""
        import asyncio

        # Create projects
        _ = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Zebra Project", owner_id=test_user.id),
        )
        await asyncio.sleep(0.01)
        _ = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Alpha Project", owner_id=test_user.id),
        )

        # Sort by name ascending
        projects_asc = await crud_project.get_multi_filtered(
            db_session, sort_by="name", sort_dir="asc", skip=0, limit=10
        )

        assert projects_asc[0].name == "Alpha Project"
        assert projects_asc[1].name == "Zebra Project"

        # Sort by name descending
        projects_desc = await crud_project.get_multi_filtered(
            db_session, sort_by="name", sort_dir="desc", skip=0, limit=10
        )

        assert projects_desc[0].name == "Zebra Project"
        assert projects_desc[1].name == "Alpha Project"

    async def test_get_count_filtered(self, db_session: AsyncSession, test_user: User):
        """Test getting count of filtered projects."""
        # Create projects
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(
                name="Project A", status="active", owner_id=test_user.id
            ),
        )
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(
                name="Project B", status="active", owner_id=test_user.id
            ),
        )
        await crud_project.create(
            db_session,
            obj_in=ProjectCreate(
                name="Project C", status="archived", owner_id=test_user.id
            ),
        )

        # Count all projects
        total_count = await crud_project.get_count_filtered(db_session)
        assert total_count == 3

        # Count active projects
        active_count = await crud_project.get_count_filtered(
            db_session, status="active"
        )
        assert active_count == 2

        # Count projects with search
        search_count = await crud_project.get_count_filtered(
            db_session, search="Project A"
        )
        assert search_count == 1

    async def test_pagination(self, db_session: AsyncSession, test_user: User):
        """Test pagination of projects."""
        # Create 5 projects
        for i in range(5):
            await crud_project.create(
                db_session,
                obj_in=ProjectCreate(name=f"Project {i}", owner_id=test_user.id),
            )

        # Get first page (2 items)
        page1 = await crud_project.get_multi_filtered(db_session, skip=0, limit=2)
        assert len(page1) == 2

        # Get second page
        page2 = await crud_project.get_multi_filtered(db_session, skip=2, limit=2)
        assert len(page2) == 2

        # Ensure different projects
        page1_ids = {p.id for p in page1}
        page2_ids = {p.id for p in page2}
        assert page1_ids.isdisjoint(page2_ids)
