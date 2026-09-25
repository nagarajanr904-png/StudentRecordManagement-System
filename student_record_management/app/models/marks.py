"""
Marks and examination results entity model.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Marks:
    """Represents subject examination score and computed grade."""

    id: Optional[int] = None
    student_id: int = 0
    subject: str = ""
    exam_name: str = ""
    marks_obtained: float = 0.0
    max_marks: float = 100.0
    percentage: float = 0.0
    grade: str = "F"
    remarks: Optional[str] = None
    created_at: Optional[Any] = None
    updated_at: Optional[Any] = None
    # Joined fields
    student_name: str = ""
    admission_number: str = ""
    department_name: str = ""

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Marks":
        """Constructs a Marks instance from row dictionary."""
        first = data.get("first_name", "")
        last = data.get("last_name", "")
        full_name = f"{first} {last}".strip() if (first or last) else str(data.get("student_name", ""))

        return cls(
            id=data.get("id"),
            student_id=int(data.get("student_id", 0)),
            subject=str(data.get("subject", "")),
            exam_name=str(data.get("exam_name", "")),
            marks_obtained=float(data.get("marks_obtained", 0.0)),
            max_marks=float(data.get("max_marks", 100.0)),
            percentage=float(data.get("percentage", 0.0)),
            grade=str(data.get("grade", "F")),
            remarks=str(data.get("remarks", "")) if data.get("remarks") is not None else None,
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            student_name=full_name,
            admission_number=str(data.get("admission_number", "")),
            department_name=str(data.get("department_name", "")),
        )
