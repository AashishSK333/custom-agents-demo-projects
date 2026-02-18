"""Application configuration loader.

Reads settings from environment variables with sensible defaults.
This module is intentionally clean — no bugs here.
"""

import os


def get_config():
    """Return the application configuration dictionary."""
    return {
        "app_name": os.environ.get("APP_NAME", "TaskTracker"),
        "debug": os.environ.get("DEBUG", "false").lower() == "true",
        "max_tasks": int(os.environ.get("MAX_TASKS", "100")),
        "log_level": os.environ.get("LOG_LEVEL", "INFO"),
        "version": "1.0.0",
    }


def is_debug():
    """Check if debug mode is enabled."""
    return get_config()["debug"]
