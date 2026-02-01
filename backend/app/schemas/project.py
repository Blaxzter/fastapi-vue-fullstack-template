import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

ProjectStatus = Literal["active", "archived"]


class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Project name")
    description: str | None = Field(
        default=None, max_length=1000, description="Project description"
    )
    status: ProjectStatus = Field(default="active", description="Project status")
    owner_id: uuid.UUID | None = Field(default=None, description="Owner user ID")


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None, min_length=1, max_length=200, description="Project name"
    )
    description: str | None = Field(
        default=None, max_length=1000, description="Project description"
    )
    status: ProjectStatus | None = Field(default=None, description="Project status")
    owner_id: uuid.UUID | None = Field(default=None, description="Owner user ID")


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ProjectListResponse(BaseModel):
    items: list[ProjectRead]
    total: int
    skip: int
    limit: int
