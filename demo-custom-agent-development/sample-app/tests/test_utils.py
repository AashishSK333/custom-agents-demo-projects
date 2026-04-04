"""Tests for utils.py.

NOTE FOR LEARNERS: Two tests here intentionally FAIL to demonstrate
how the Code Review Assistant uses the `runTests` and `testFailure`
tools to detect and diagnose issues:
  - test_safe_divide_by_zero  — expects ZeroDivisionError but gets 0
  - test_format_user_name_none — expects graceful handling of None
"""

import pytest
from datetime import datetime
from utils import (
    find_duplicates,
    parse_date,
    safe_divide,
    format_user_name,
    truncate_string,
)


# --- find_duplicates ---

def test_find_duplicates_basic():
    assert find_duplicates([1, 2, 3, 2, 4, 3]) == [2, 3]


def test_find_duplicates_no_dupes():
    assert find_duplicates([1, 2, 3]) == []


def test_find_duplicates_all_same():
    assert find_duplicates(["a", "a", "a"]) == ["a"]


def test_find_duplicates_empty():
    assert find_duplicates([]) == []


# --- parse_date ---

def test_parse_date_valid():
    result = parse_date("2025-06-15")
    assert result == datetime(2025, 6, 15)


def test_parse_date_invalid():
    assert parse_date("not-a-date") is None


def test_parse_date_wrong_format():
    assert parse_date("15/06/2025") is None


# --- safe_divide ---

def test_safe_divide_normal():
    assert safe_divide(10, 2) == 5.0


def test_safe_divide_float():
    assert safe_divide(7, 3) == pytest.approx(2.3333, rel=1e-3)


def test_safe_divide_by_zero():
    """INTENTIONALLY FAILS: safe_divide returns 0 instead of raising."""
    with pytest.raises(ZeroDivisionError):
        safe_divide(10, 0)


# --- format_user_name ---

def test_format_user_name_basic():
    assert format_user_name("Jane", "Doe") == "Jane Doe"


def test_format_user_name_whitespace():
    assert format_user_name("  Jane  ", "  Doe  ") == "Jane Doe"


def test_format_user_name_none():
    """INTENTIONALLY FAILS: format_user_name crashes on None input."""
    result = format_user_name(None, "Doe")
    assert result == "Doe"


# --- truncate_string ---

def test_truncate_short():
    assert truncate_string("hello", 50) == "hello"


def test_truncate_long():
    assert truncate_string("a" * 100, 50) == "a" * 47 + "..."


def test_truncate_exact():
    assert truncate_string("a" * 50, 50) == "a" * 50
