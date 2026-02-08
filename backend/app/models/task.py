import uuid
from datetime import date
from typing import TYPE_CHECKING, Optional

import sqlalchemy as sa
from sqlmodel import Field, Relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.project import Project


class Task(Base, table=True):
    __tablename__ = "tasks"

    project_id: uuid.UUID = Field(
        foreign_key="projects.id",
        index=True,
        description="Parent project ID",
    )
    title: str = Field(
        sa_column=sa.Column(sa.String, nullable=False, index=True),
        description="Task title",
    )
    description: str | None = Field(
        default=None,
        sa_column=sa.Column(sa.Text),
        description="Task description",
    )
    status: str = Field(
        default="todo",
        sa_column=sa.Column(sa.String, nullable=False, index=True),
        description="Task status",
    )
    priority: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Task priority (1-5)",
    )
    due_date: date | None = Field(
        default=None,
        description="Optional due date",
    )

    project: Optional["Project"] = Relationship(back_populates="tasks")
