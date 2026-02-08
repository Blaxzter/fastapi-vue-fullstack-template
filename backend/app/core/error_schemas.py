"""
OpenAPI error schemas and response definitions for consistent error handling.

This module contains the ProblemDetails schema definitions and standard error responses
used throughout the API to ensure consistent error reporting in the OpenAPI spec.
"""

from app.core.errors import PROBLEM_JSON_MEDIA_TYPE

# OpenAPI schema for validation error items
VALIDATION_ERROR_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "loc": {
            "type": "array",
            "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
        },
        "msg": {"type": "string"},
        "type": {"type": "string"},
    },
    "required": ["loc", "msg", "type"],
}

# OpenAPI schema for ProblemDetails (RFC 7807)
PROBLEM_DETAILS_SCHEMA = {
    "type": "object",
    "properties": {
        "type": {"type": "string", "format": "uri", "default": "about:blank"},
        "code": {"type": "string"},
        "title": {"type": "string"},
        "status": {"type": "integer"},
        "detail": {"type": "string"},
        "instance": {"type": "string"},
        "errors": {
            "type": "array",
            "items": {"$ref": "#/components/schemas/ValidationErrorItem"},
        },
    },
    "required": ["type", "title", "status"],
}


def get_openapi_schemas() -> dict:
    """
    Returns the OpenAPI component schemas for error handling.

    Returns:
        dict: Dictionary containing ValidationErrorItem and ProblemDetails schemas
    """
    return {
        "ValidationErrorItem": VALIDATION_ERROR_ITEM_SCHEMA,
        "ProblemDetails": PROBLEM_DETAILS_SCHEMA,
    }


# Reference to ProblemDetails schema for reuse in responses
PROBLEM_DETAILS_REF = {"$ref": "#/components/schemas/ProblemDetails"}

# Standard error responses for OpenAPI documentation
ERROR_RESPONSES = {
    400: {
        "description": "Bad Request",
        "content": {PROBLEM_JSON_MEDIA_TYPE: {"schema": PROBLEM_DETAILS_REF}},
    },
    401: {
        "description": "Unauthorized",
        "content": {PROBLEM_JSON_MEDIA_TYPE: {"schema": PROBLEM_DETAILS_REF}},
    },
    403: {
        "description": "Forbidden",
        "content": {PROBLEM_JSON_MEDIA_TYPE: {"schema": PROBLEM_DETAILS_REF}},
    },
    404: {
        "description": "Not Found",
        "content": {PROBLEM_JSON_MEDIA_TYPE: {"schema": PROBLEM_DETAILS_REF}},
    },
    409: {
        "description": "Conflict",
        "content": {PROBLEM_JSON_MEDIA_TYPE: {"schema": PROBLEM_DETAILS_REF}},
    },
    422: {
        "description": "Validation Error",
        "content": {PROBLEM_JSON_MEDIA_TYPE: {"schema": PROBLEM_DETAILS_REF}},
    },
    429: {
        "description": "Too Many Requests",
        "content": {PROBLEM_JSON_MEDIA_TYPE: {"schema": PROBLEM_DETAILS_REF}},
    },
    500: {
        "description": "Internal Server Error",
        "content": {PROBLEM_JSON_MEDIA_TYPE: {"schema": PROBLEM_DETAILS_REF}},
    },
}
