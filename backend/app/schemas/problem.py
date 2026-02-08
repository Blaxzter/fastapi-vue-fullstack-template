from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ValidationErrorItem(BaseModel):
    loc: list[str | int] = Field(default_factory=list)
    msg: str
    type: str


class ProblemDetails(BaseModel):
    model_config = ConfigDict(extra="allow")

    type: str = Field(default="about:blank")
    code: str | None = None
    title: str
    status: int
    detail: str | None = None
    instance: str | None = None
    errors: list[ValidationErrorItem] | None = None


def coerce_problem_detail(detail: Any) -> str | None:
    if detail is None:
        return None
    if isinstance(detail, str):
        return detail
    return str(detail)
