"""Unit tests for Task CRUD operations."""

from datetime import date

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.task import task as crud_task
from app.models.project import Project
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


@pytest.mark.asyncio
class TestTaskCRUD:
    """Test suite for Task CRUD operations."""

    async def test_create_task(self, db_session: AsyncSession, test_project: Project):
        """Test creating a new task."""
        task_in = TaskCreate(
            project_id=test_project.id,
            title="New Task",
            description="A brand new task",
            status="todo",
            priority=4,
            due_date=date(2026, 12, 25),
        )
        task = await crud_task.create(db_session, obj_in=task_in)

        assert task.title == "New Task"
        assert task.description == "A brand new task"
        assert task.status == "todo"
        assert task.priority == 4
        assert task.due_date == date(2026, 12, 25)
        assert task.project_id == test_project.id
        assert task.id is not None

    async def test_create_task_minimal(
        self, db_session: AsyncSession, test_project: Project
    ):
        """Test creating a task with minimal fields."""
        task_in = TaskCreate(
            project_id=test_project.id,
            title="Minimal Task",
        )
        task = await crud_task.create(db_session, obj_in=task_in)

        assert task.title == "Minimal Task"
        assert task.status == "todo"  # Default value
        assert task.priority == 3  # Default value
        assert task.due_date is None

    async def test_get_task(self, db_session: AsyncSession, test_task: Task):
        """Test getting a task by ID."""
        task = await crud_task.get(db_session, id=test_task.id)

        assert task is not None
        assert task.id == test_task.id
        assert task.title == test_task.title

    async def test_get_task_not_found(self, db_session: AsyncSession):
        """Test getting a non-existent task."""
        import uuid

        fake_id = uuid.uuid4()
        task = await crud_task.get(db_session, id=fake_id)

        assert task is None

    async def test_get_task_not_found_with_error(self, db_session: AsyncSession):
        """Test getting a non-existent task with raise_404_error=True."""
        import uuid

        fake_id = uuid.uuid4()
        with pytest.raises(HTTPException) as exc_info:
            await crud_task.get(db_session, id=fake_id, raise_404_error=True)

        assert exc_info.value.status_code == 404
        assert "Task not found" in str(exc_info.value.detail)

    async def test_get_multi_tasks(
        self, db_session: AsyncSession, multiple_test_tasks: list[Task]
    ):
        """Test getting multiple tasks."""
        tasks = await crud_task.get_multi(db_session, skip=0, limit=10)

        assert len(tasks) == 5

    async def test_update_task(self, db_session: AsyncSession, test_task: Task):
        """Test updating a task."""
        task_update = TaskUpdate(
            title="Updated Task",
            description="Updated description",
            priority=5,
        )
        updated_task = await crud_task.update(
            db_session, db_obj=test_task, obj_in=task_update
        )

        assert updated_task.id == test_task.id
        assert updated_task.title == "Updated Task"
        assert updated_task.description == "Updated description"
        assert updated_task.priority == 5

    async def test_update_task_status(self, db_session: AsyncSession, test_task: Task):
        """Test updating task status."""
        task_update = TaskUpdate(status="done")
        updated_task = await crud_task.update(
            db_session, db_obj=test_task, obj_in=task_update
        )

        assert updated_task.status == "done"

    async def test_remove_task(self, db_session: AsyncSession, test_task: Task):
        """Test removing a task."""
        task_id = test_task.id
        removed_task = await crud_task.remove(db_session, id=task_id)

        assert removed_task is not None
        assert removed_task.id == task_id

        # Verify task is deleted
        task = await crud_task.get(db_session, id=task_id)
        assert task is None

    async def test_get_multi_filtered_by_search(
        self, db_session: AsyncSession, test_project: Project
    ):
        """Test filtering tasks by search query."""
        # Create tasks with specific titles
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(
                project_id=test_project.id,
                title="Implement feature A",
                description="Feature description",
            ),
        )
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(
                project_id=test_project.id,
                title="Fix bug B",
                description="Bug description",
            ),
        )
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(
                project_id=test_project.id,
                title="Write docs",
                description="Documentation feature",
            ),
        )

        # Search for "feature"
        tasks = await crud_task.get_multi_filtered(
            db_session, search="feature", skip=0, limit=10
        )

        assert len(tasks) == 2  # Matches title and description
        task_titles = [t.title for t in tasks]
        assert "Implement feature A" in task_titles
        assert "Write docs" in task_titles

    async def test_get_multi_filtered_by_status(
        self, db_session: AsyncSession, multiple_test_tasks: list[Task]
    ):
        """Test filtering tasks by status."""
        # Tasks have alternating statuses (todo/in_progress)
        todo_tasks = await crud_task.get_multi_filtered(
            db_session, status="todo", skip=0, limit=10
        )

        in_progress_tasks = await crud_task.get_multi_filtered(
            db_session, status="in_progress", skip=0, limit=10
        )

        assert len(todo_tasks) == 3  # 0, 2, 4
        assert len(in_progress_tasks) == 2  # 1, 3
        assert all(t.status == "todo" for t in todo_tasks)
        assert all(t.status == "in_progress" for t in in_progress_tasks)

    async def test_get_multi_filtered_by_project(
        self, db_session: AsyncSession, test_user
    ):
        """Test filtering tasks by project."""
        from app.crud.project import project as crud_project
        from app.schemas.project import ProjectCreate

        # Create two projects
        project1 = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Project 1", owner_id=test_user.id),
        )
        project2 = await crud_project.create(
            db_session,
            obj_in=ProjectCreate(name="Project 2", owner_id=test_user.id),
        )

        # Create tasks for different projects
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(project_id=project1.id, title="Task P1-1"),
        )
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(project_id=project1.id, title="Task P1-2"),
        )
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(project_id=project2.id, title="Task P2-1"),
        )

        # Filter by project1
        project1_tasks = await crud_task.get_multi_filtered(
            db_session, project_id=project1.id, skip=0, limit=10
        )

        assert len(project1_tasks) == 2
        assert all(t.project_id == project1.id for t in project1_tasks)

        # Filter by project2
        project2_tasks = await crud_task.get_multi_filtered(
            db_session, project_id=project2.id, skip=0, limit=10
        )

        assert len(project2_tasks) == 1
        assert project2_tasks[0].project_id == project2.id

    async def test_get_multi_filtered_with_sorting(
        self, db_session: AsyncSession, test_project: Project
    ):
        """Test sorting tasks."""
        # Create tasks with different priorities
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(
                project_id=test_project.id, title="Low Priority", priority=1
            ),
        )
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(
                project_id=test_project.id, title="High Priority", priority=5
            ),
        )
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(
                project_id=test_project.id, title="Medium Priority", priority=3
            ),
        )

        # Sort by priority ascending
        tasks_asc = await crud_task.get_multi_filtered(
            db_session, sort_by="priority", sort_dir="asc", skip=0, limit=10
        )

        assert tasks_asc[0].priority == 1
        assert tasks_asc[1].priority == 3
        assert tasks_asc[2].priority == 5

        # Sort by priority descending
        tasks_desc = await crud_task.get_multi_filtered(
            db_session, sort_by="priority", sort_dir="desc", skip=0, limit=10
        )

        assert tasks_desc[0].priority == 5
        assert tasks_desc[1].priority == 3
        assert tasks_desc[2].priority == 1

    async def test_get_multi_filtered_sort_by_title(
        self, db_session: AsyncSession, test_project: Project
    ):
        """Test sorting tasks by title."""
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(project_id=test_project.id, title="Zebra Task"),
        )
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(project_id=test_project.id, title="Alpha Task"),
        )

        # Sort by title ascending
        tasks = await crud_task.get_multi_filtered(
            db_session, sort_by="title", sort_dir="asc", skip=0, limit=10
        )

        assert tasks[0].title == "Alpha Task"
        assert tasks[1].title == "Zebra Task"

    async def test_get_count_filtered(
        self, db_session: AsyncSession, test_project: Project
    ):
        """Test getting count of filtered tasks."""
        # Create tasks
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(
                project_id=test_project.id, title="Task A", status="todo"
            ),
        )
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(
                project_id=test_project.id, title="Task B", status="todo"
            ),
        )
        await crud_task.create(
            db_session,
            obj_in=TaskCreate(
                project_id=test_project.id, title="Task C", status="done"
            ),
        )

        # Count all tasks
        total_count = await crud_task.get_count_filtered(db_session)
        assert total_count == 3

        # Count todo tasks
        todo_count = await crud_task.get_count_filtered(db_session, status="todo")
        assert todo_count == 2

        # Count tasks with search
        search_count = await crud_task.get_count_filtered(db_session, search="Task A")
        assert search_count == 1

    async def test_pagination(self, db_session: AsyncSession, test_project: Project):
        """Test pagination of tasks."""
        # Create 5 tasks
        for i in range(5):
            await crud_task.create(
                db_session,
                obj_in=TaskCreate(project_id=test_project.id, title=f"Task {i}"),
            )

        # Get first page (2 items)
        page1 = await crud_task.get_multi_filtered(db_session, skip=0, limit=2)
        assert len(page1) == 2

        # Get second page
        page2 = await crud_task.get_multi_filtered(db_session, skip=2, limit=2)
        assert len(page2) == 2

        # Ensure different tasks
        page1_ids = {t.id for t in page1}
        page2_ids = {t.id for t in page2}
        assert page1_ids.isdisjoint(page2_ids)

    async def test_task_with_due_date(
        self, db_session: AsyncSession, test_project: Project
    ):
        """Test task with due date."""
        due = date(2027, 1, 15)
        task_in = TaskCreate(
            project_id=test_project.id,
            title="Task with deadline",
            due_date=due,
        )
        task = await crud_task.create(db_session, obj_in=task_in)

        assert task.due_date == due

        # Update due date
        new_due = date(2027, 2, 20)
        task_update = TaskUpdate(due_date=new_due)
        updated_task = await crud_task.update(
            db_session, db_obj=task, obj_in=task_update
        )

        assert updated_task.due_date == new_due
