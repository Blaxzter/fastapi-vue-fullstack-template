from __future__ import annotations

from http import HTTPStatus

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.schemas.problem import (
    ProblemDetails,
    ValidationErrorItem,
    coerce_problem_detail,
)

PROBLEM_JSON_MEDIA_TYPE = "application/problem+json"


def _status_title(status_code: int) -> str:
    try:
        return HTTPStatus(status_code).phrase
    except ValueError:
        return "Error"


def _problem_response(
    *,
    status_code: int,
    title: str,
    detail: str | None,
    instance: str | None,
    errors: list[ValidationErrorItem] | None = None,
    code: str | None = None,
    headers: dict[str, str] | None = None,
    type_url: str = "about:blank",
) -> JSONResponse:
    payload = ProblemDetails(
        type=type_url,
        code=code,
        title=title,
        status=status_code,
        detail=detail,
        instance=instance,
        errors=errors,
    )
    return JSONResponse(
        status_code=status_code,
        content=payload.model_dump(exclude_none=True),
        headers=headers,
        media_type=PROBLEM_JSON_MEDIA_TYPE,
    )


def _normalize_validation_errors(
    exc: RequestValidationError,
) -> list[ValidationErrorItem]:
    items: list[ValidationErrorItem] = []
    for error in exc.errors():
        loc = error.get("loc", [])
        items.append(
            ValidationErrorItem(
                loc=[
                    part if isinstance(part, str | int) else str(part) for part in loc
                ],
                msg=str(error.get("msg", "Invalid value")),
                type=str(error.get("type", "value_error")),
            )
        )
    return items


def _parse_problem_detail(detail: object) -> tuple[str | None, str | None, str | None]:
    if isinstance(detail, dict):
        code = detail.get("code")
        code_value = code if isinstance(code, str) else None
        type_url = detail.get("type")
        type_value = type_url if isinstance(type_url, str) else None
        if not type_value and code_value:
            type_value = f"urn:problem:{code_value}"
        detail_value = detail.get("detail")
        if not isinstance(detail_value, str):
            detail_value = (
                detail.get("message")
                if isinstance(detail.get("message"), str)
                else None
            )
        return detail_value, type_value, code_value
    return coerce_problem_detail(detail), None, None


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    status_code = exc.status_code
    detail, type_url, code = _parse_problem_detail(exc.detail)
    if not detail:
        detail = _status_title(status_code)
    return _problem_response(
        status_code=status_code,
        title=_status_title(status_code),
        detail=detail,
        instance=str(request.url.path),
        code=code,
        headers=exc.headers,
        type_url=type_url or "about:blank",
    )


def starlette_http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    status_code = exc.status_code
    detail, type_url, code = _parse_problem_detail(exc.detail)
    if not detail:
        detail = _status_title(status_code)
    return _problem_response(
        status_code=status_code,
        title=_status_title(status_code),
        detail=detail,
        instance=str(request.url.path),
        code=code,
        headers=exc.headers,
        type_url=type_url or "about:blank",
    )


def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return _problem_response(
        status_code=422,
        title="Validation Error",
        detail="Request validation failed.",
        instance=str(request.url.path),
        errors=_normalize_validation_errors(exc),
    )


def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if settings.ENVIRONMENT == "local":
        detail = f"{type(exc).__name__}: {exc}"
    else:
        detail = "Unexpected error occurred."
    return _problem_response(
        status_code=500,
        title=_status_title(500),
        detail=detail,
        instance=str(request.url.path),
    )


def problem_detail(
    *, code: str, detail: str | None = None, type_url: str | None = None
) -> dict[str, str]:
    payload = {"code": code, "type": type_url or f"urn:problem:{code}"}
    if detail:
        payload["detail"] = detail
    return payload


def raise_problem(
    status_code: int,
    *,
    code: str,
    detail: str | None = None,
    headers: dict[str, str] | None = None,
) -> None:
    raise HTTPException(
        status_code=status_code,
        detail=problem_detail(code=code, detail=detail),
        headers=headers,
    )
