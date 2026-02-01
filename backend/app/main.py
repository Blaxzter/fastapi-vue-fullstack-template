import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute

from app.api.api import api_router
from app.core.config import settings
from app.core.logger import get_logger
from app.core.middleware import RequestLoggingMiddleware

# Configure logging levels for various loggers
logger = get_logger("main")

# Configure logging levels for third-party libraries to reduce noise
LOGGER_LEVELS = {
    "httpcore.http11": logging.WARNING,
    "httpcore.connection": logging.WARNING,
    "httpx": logging.WARNING,
    "uvicorn.access": logging.WARNING,  # Disable default uvicorn request logging (we use our custom logger)
    "sqlalchemy.engine": logging.WARNING,
}

for logger_name, level in LOGGER_LEVELS.items():
    logging.getLogger(logger_name).setLevel(level)


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    import sentry_sdk

    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)


def custom_openapi():
    """
    Custom OpenAPI function to add HTTPException schema
    This allows us to generate a frontend client with the HTTPException schema for type safe error handling
    """
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    # Add HTTPException schema
    # Add HTTPException schema
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}
    if "schemas" not in openapi_schema["components"]:
        openapi_schema["components"]["schemas"] = {}

    openapi_schema["components"]["schemas"]["HTTPException"] = {
        "type": "object",
        "properties": {"detail": {"type": "string"}},
        "required": ["detail"],
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

app.openapi = custom_openapi

# Add request logging middleware (must be added before other middleware)
app.add_middleware(RequestLoggingMiddleware)

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(
    api_router,
    prefix=settings.API_V1_STR,
    responses={
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/HTTPException"}
                }
            },
        },
    },
)


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting FastAPI application")

    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=True,
    )
