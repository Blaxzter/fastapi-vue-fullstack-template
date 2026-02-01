import uuid
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

TaskStatus = Literal["todo", "in_progress", "done"]


class TaskBase(BaseModel):
    project_id: uuid.UUID = Field(..., description="Parent project ID")
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str | None = Field(
        default=None, max_length=2000, description="Task description"
    )
    status: TaskStatus = Field(default="todo", description="Task status")
    priority: int = Field(default=3, ge=1, le=5, description="Task priority (1-5)")
    due_date: date | None = Field(default=None, description="Optional due date")


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None, min_length=1, max_length=200, description="Task title"
    )
    description: str | None = Field(
        default=None, max_length=2000, description="Task description"
    )
    status: TaskStatus | None = Field(default=None, description="Task status")
    priority: int | None = Field(default=None, ge=1, le=5, description="Task priority")
    due_date: date | None = Field(default=None, description="Optional due date")
    project_id: uuid.UUID | None = Field(default=None, description="Parent project ID")


class TaskRead(TaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TaskListResponse(BaseModel):
    items: list[TaskRead]
    total: int
    skip: int
    limit: int
