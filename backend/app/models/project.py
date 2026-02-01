import uuid
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlmodel import Field, Relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.task import Task


class Project(Base, table=True):
    __tablename__ = "projects"

    name: str = Field(
        sa_column=sa.Column(sa.String, nullable=False, index=True),
        description="Project name",
    )
    description: str | None = Field(
        default=None,
        sa_column=sa.Column(sa.Text),
        description="Short project description",
    )
    status: str = Field(
        default="active",
        sa_column=sa.Column(sa.String, nullable=False, index=True),
        description="Project status",
    )
    owner_id: uuid.UUID | None = Field(
        default=None,
        foreign_key="users.id",
        index=True,
        description="Owning user ID",
    )

    tasks: list["Task"] = Relationship(
        back_populates="project",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
