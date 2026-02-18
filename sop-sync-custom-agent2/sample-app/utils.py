"""Utility functions for the task tracker.

NOTE FOR LEARNERS: This file contains intentional bugs and anti-patterns
that the Code Review Assistant agent is designed to catch:
  1. find_duplicates  — O(n^2) performance anti-pattern
  2. parse_date       — Bare except swallowing all exceptions
  3. safe_divide      — Logic bug: silently returns 0 on division by zero
  4. format_user_name — Missing input validation for None values
"""

from datetime import datetime


def find_duplicates(items):
    """Return a list of duplicate items.

    BUG: Uses O(n^2) nested loop. A set-based approach would be O(n).
    """
    duplicates = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j] and items[i] not in duplicates:
                duplicates.append(items[i])
    return duplicates


def parse_date(date_str):
    """Parse a date string in YYYY-MM-DD format.

    BUG: Bare except clause swallows ALL exceptions (KeyboardInterrupt,
    SystemExit, MemoryError, etc.) — should catch ValueError only.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None


def safe_divide(a, b):
    """Divide a by b safely.

    BUG: Returns 0 when b is 0 instead of raising ZeroDivisionError.
    This silently hides errors — callers can't distinguish "result is 0"
    from "division was impossible." Should raise or return a sentinel.
    """
    if b == 0:
        return 0
    return a / b


def format_user_name(first, last):
    """Format a user's full name.

    BUG: No validation for None inputs. Calling str.strip() on None
    will raise AttributeError.
    """
    return f"{first.strip()} {last.strip()}"


def truncate_string(text, max_length=50):
    """Truncate a string to max_length, adding ellipsis if needed."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
