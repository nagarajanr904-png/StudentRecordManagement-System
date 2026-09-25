"""
Helper utility functions for grading, dates, formatting, and file exports.
"""

import csv
from datetime import date, datetime
from typing import Any, List, Optional
from app.utils.constants import GRADE_SCALE


def calculate_grade(percentage: float) -> str:
    """
    Computes letter grade from percentage based on standard academic scale:
    >= 90%: A+
    >= 80%: A
    >= 70%: B
    >= 60%: C
    >= 50%: D
    < 50%: F
    """
    for threshold, letter in GRADE_SCALE:
        if percentage >= threshold:
            return letter
    return "F"


def format_date_display(val: Any) -> str:
    """Formats a date object or ISO string to friendly display format: YYYY-MM-DD."""
    if not val:
        return "N/A"
    if isinstance(val, (date, datetime)):
        return val.strftime("%Y-%m-%d")
    return str(val)


def export_to_csv(filepath: str, headers: List[str], rows: List[List[Any]]) -> bool:
    """Exports structured data to CSV file with utf-8 encoding."""
    try:
        with open(filepath, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for row in rows:
                writer.writerow([str(item) if item is not None else "" for item in row])
        return True
    except Exception:
        return False


def sanitize_input(value: Optional[str]) -> str:
    """Strips leading/trailing whitespaces and normalizes blank strings."""
    if value is None:
        return ""
    return str(value).strip()
