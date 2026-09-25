"""
Attendance entity model.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Attendance:
    """Represents a single daily attendance record for a student."""

    id: Optional[int] = None
    student_id: int = 0
    attendance_date: str = ""
    status: str = "Present"  # Present, Absent, Late
    remarks: Optional[str] = None
    created_at: Optional[Any] = None
    updated_at: Optional[Any] = None
    # Joined fields for presentation
    student_name: str = ""
    admission_number: str = ""
    department_name: str = ""
    year: int = 1

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Attendance":
        """Constructs an Attendance instance from row dictionary."""
        first = data.get("first_name", "")
        last = data.get("last_name", "")
        full_name = f"{first} {last}".strip() if (first or last) else str(data.get("student_name", ""))

        return cls(
            id=data.get("id"),
            student_id=int(data.get("student_id", 0)),
            attendance_date=str(data.get("attendance_date", "")),
            status=str(data.get("status", "Present")),
            remarks=str(data.get("remarks", "")) if data.get("remarks") is not None else None,
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            student_name=full_name,
            admission_number=str(data.get("admission_number", "")),
            department_name=str(data.get("department_name", "")),
            year=int(data.get("year", 1)),
        )
