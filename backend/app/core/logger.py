"""
Logger utility for the application
Provides colored console logging with proper formatting
"""

import logging
import sys


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels"""

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"
    BOLD = "\033[1m"

    def format(self, record: logging.LogRecord) -> str:
        # Add color to the level name
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[levelname]}{self.BOLD}{levelname}{self.RESET}"
            )
        return super().format(record)


def get_logger(
    name: str,
    level: int = logging.INFO,
    format_string: str | None = None,
) -> logging.Logger:
    """
    Get a configured logger instance with colored output

    Args:
        name: Logger name (usually __name__ or a descriptive string)
        level: Logging level (default: INFO)
        format_string: Custom format string (optional)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Use custom format or default
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Add colored formatter
    formatter = ColoredFormatter(format_string)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
