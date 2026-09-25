"""
Validation logic for student, attendance, marks, and department entities.
Provides clear, human-understandable error messages.
"""

import re
from datetime import datetime
from typing import Optional, Tuple


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PHONE_REGEX = re.compile(r"^[+]?[\d\s\-().]{7,25}$")


def validate_required(value: Optional[str], field_name: str) -> Tuple[bool, str]:
    """Validates that a string is non-empty after trimming."""
    if not value or not str(value).strip():
        return False, f"{field_name} is required."
    return True, ""


def validate_email(email: Optional[str]) -> Tuple[bool, str]:
    """Validates standard email address format."""
    if not email or not email.strip():
        return False, "Email address is required."
    clean_email = email.strip()
    if not EMAIL_REGEX.match(clean_email):
        return False, "Please enter a valid email address (e.g. student@domain.edu)."
    return True, ""


def validate_phone(phone: Optional[str], field_name: str = "Phone number") -> Tuple[bool, str]:
    """Validates phone number format."""
    if not phone or not phone.strip():
        return False, f"{field_name} is required."
    clean_phone = phone.strip()
    digits_only = re.sub(r"\D", "", clean_phone)
    if len(digits_only) < 7:
        return False, f"{field_name} must contain at least 7 digits."
    if not PHONE_REGEX.match(clean_phone):
        return False, f"{field_name} contains invalid characters."
    return True, ""


def validate_date(date_str: Optional[str], field_name: str = "Date") -> Tuple[bool, str]:
    """Validates date format in YYYY-MM-DD format."""
    if not date_str or not date_str.strip():
        return False, f"{field_name} is required."
    clean_date = date_str.strip()
    try:
        parsed_date = datetime.strptime(clean_date, "%Y-%m-%d").date()
        if parsed_date.year < 1900 or parsed_date.year > 2100:
            return False, f"{field_name} year must be between 1900 and 2100."
        return True, ""
    except ValueError:
        return False, f"{field_name} must be in YYYY-MM-DD format (e.g. 2004-05-15)."


def validate_academic_year(year: Optional[int]) -> Tuple[bool, str]:
    """Validates academic year (typically 1 to 4)."""
    if year is None:
        return False, "Academic year is required."
    try:
        yr = int(year)
        if yr < 1 or yr > 8:
            return False, "Academic year must be between 1 and 8."
        return True, ""
    except (ValueError, TypeError):
        return False, "Academic year must be a valid integer."


def validate_marks(
    obtained_str: Optional[str], max_marks_str: Optional[str] = "100.00"
) -> Tuple[bool, str, float, float]:
    """
    Validates marks entered:
    - Must be numeric
    - Cannot be negative
    - Cannot exceed maximum marks
    Returns (is_valid, error_message, obtained_float, max_float).
    """
    if not obtained_str or not str(obtained_str).strip():
        return False, "Marks obtained is required.", 0.0, 100.0

    try:
        obtained = float(obtained_str.strip())
    except ValueError:
        return False, "Marks obtained must be a numeric value.", 0.0, 100.0

    try:
        max_marks = float(str(max_marks_str).strip()) if max_marks_str else 100.0
    except ValueError:
        return False, "Maximum marks must be a numeric value.", 0.0, 100.0

    if max_marks <= 0:
        return False, "Maximum marks must be greater than zero.", obtained, max_marks

    if obtained < 0:
        return False, "Marks obtained cannot be negative.", obtained, max_marks

    if obtained > max_marks:
        return (
            False,
            f"Marks obtained ({obtained:.2f}) cannot exceed maximum marks ({max_marks:.2f}).",
            obtained,
            max_marks,
        )

    return True, "", obtained, max_marks


def validate_admission_number(adm_num: Optional[str]) -> Tuple[bool, str]:
    """Validates admission number format and presence."""
    if not adm_num or not adm_num.strip():
        return False, "Admission number is required."
    clean = adm_num.strip()
    if len(clean) < 3:
        return False, "Admission number must be at least 3 characters."
    if len(clean) > 50:
        return False, "Admission number cannot exceed 50 characters."
    return True, ""
