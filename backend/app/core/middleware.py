"""
Request logging middleware for FastAPI
Logs all incoming requests with colored output, handler location, and timing
"""

import inspect
import logging
import time
import traceback
from http import HTTPStatus

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from app.core.logger import get_logger

# Configure logger for requests
request_logger = get_logger("request", level=logging.INFO)

# Paths to ignore in logging
IGNORE_PATHS = ["/api/v1/health", "/docs", "/redoc", "/openapi.json"]


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log all HTTP requests with timing and handler information"""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """Process request and log details"""
        # Skip logging for ignored paths
        if any(request.url.path.startswith(path) for path in IGNORE_PATHS):
            return await call_next(request)

        # Skip OPTIONS requests
        if request.method == "OPTIONS":
            return await call_next(request)

        # Record start time
        start_time = time.time()

        # Process request and handle exceptions
        try:
            response = await call_next(request)
            duration = time.time() - start_time

            # Get handler location
            location = self._get_handler_location(request)

            # Get colored method
            colored_method = self._get_colored_method(request.method)

            # Get colored status
            status_display = self._get_colored_status(response.status_code)

            # Log the request
            request_logger.info(
                f"Request {colored_method} {request.url.path} - {status_display} - "
                f"Handler at {location} - {duration * 1000:.2f}ms"
            )

            return response

        except Exception as error:
            duration = time.time() - start_time

            # Get handler location
            location = self._get_handler_location(request)

            # Get colored method
            colored_method = self._get_colored_method(request.method)

            # Bright red for exceptions
            status_display = f"\033[91m\033[1m500 Internal Server Error (Exception: {str(error)})\033[0m"

            # Log the error
            request_logger.error(
                f"Request {colored_method} {request.url.path} - {status_display} - "
                f"Handler at {location} - {duration * 1000:.2f}ms"
            )

            # Log traceback if debug mode
            if request_logger.level == logging.DEBUG:
                formatted_tb = "".join(
                    traceback.format_exception(type(error), error, error.__traceback__)
                )
                request_logger.error(f"\n{formatted_tb}")

            # Re-raise the exception to be handled by FastAPI's exception handlers
            raise

    def _get_handler_location(self, request: Request) -> str:
        """Get the file path and line number of the request handler"""
        try:
            # Try to get the matched route from the request scope
            route = request.scope.get("route")
            if not route:
                return "unknown location"

            # Get the endpoint function
            endpoint = route.endpoint
            if not endpoint:
                return "unknown location"

            # Unwrap decorators to get the actual function
            while hasattr(endpoint, "__wrapped__"):
                endpoint = endpoint.__wrapped__

            # Get the module and file path
            endpoint_module = inspect.getmodule(endpoint)
            if not endpoint_module or not endpoint_module.__file__:
                return "unknown location"

            file_path = endpoint_module.__file__.replace("\\", "/")

            # Get relative path from 'app' directory
            if "/app/" in file_path:
                relative_path = "app/" + file_path.split("/app/")[1]
            elif "\\app\\" in file_path:
                relative_path = "app/" + file_path.split("\\app\\")[1].replace(
                    "\\", "/"
                )
            else:
                # If 'app' not in path, just use the filename
                relative_path = file_path.split("/")[-1]

            # Get line number
            try:
                line_number = inspect.getsourcelines(endpoint)[1]
                location = f"{relative_path}:{line_number}"
            except (OSError, TypeError):
                location = relative_path

            return location

        except Exception:
            return "unknown location"

    def _get_colored_method(self, method: str) -> str:
        """Get color-coded HTTP method string"""
        method_colors = {
            "GET": "\033[94m",  # Blue
            "POST": "\033[92m",  # Green
            "PUT": "\033[93m",  # Yellow
            "PATCH": "\033[95m",  # Magenta
            "DELETE": "\033[91m",  # Red
        }
        method_color = method_colors.get(method, "\033[37m")  # Default white
        return f"{method_color}{method.ljust(6)}\033[0m"

    def _get_colored_status(self, status_code: int) -> str:
        """Get color-coded status display string"""
        try:
            status_phrase = HTTPStatus(status_code).phrase
        except ValueError:
            status_phrase = "Unknown"

        if status_code < 300:
            # Green for success (2xx)
            status_display = f"\033[92m{status_code} {status_phrase}\033[0m"
        elif status_code < 400:
            # Yellow for redirects (3xx)
            status_display = f"\033[93m{status_code} {status_phrase}\033[0m"
        elif status_code < 500:
            # Red for client errors (4xx)
            status_display = f"\033[91m{status_code} {status_phrase}\033[0m"
        else:
            # Bright red for server errors (5xx)
            status_display = f"\033[91m\033[1m{status_code} {status_phrase}\033[0m"

        return status_display
