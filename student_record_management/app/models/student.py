"""
Student entity model.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Student:
    """Represents a student enrolled in an academic institution."""

    id: Optional[int] = None
    admission_number: str = ""
    first_name: str = ""
    last_name: str = ""
    gender: str = "Male"
    date_of_birth: str = ""
    phone_number: str = ""
    email: str = ""
    address: str = ""
    department_id: int = 1
    year: int = 1
    guardian_name: str = ""
    guardian_phone: str = ""
    admission_date: str = ""
    status: str = "Active"
    created_date: Optional[Any] = None
    updated_date: Optional[Any] = None
    # Joined presentation fields
    department_name: str = ""
    department_code: str = ""

    @property
    def full_name(self) -> str:
        """Returns the full name of the student."""
        return f"{self.first_name} {self.last_name}".strip()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """Constructs a Student instance from database row dictionary."""
        return cls(
            id=data.get("id"),
            admission_number=str(data.get("admission_number", "")),
            first_name=str(data.get("first_name", "")),
            last_name=str(data.get("last_name", "")),
            gender=str(data.get("gender", "Male")),
            date_of_birth=str(data.get("date_of_birth", "")),
            phone_number=str(data.get("phone_number", "")),
            email=str(data.get("email", "")),
            address=str(data.get("address", "")),
            department_id=int(data.get("department_id", 1)),
            year=int(data.get("year", 1)),
            guardian_name=str(data.get("guardian_name", "")),
            guardian_phone=str(data.get("guardian_phone", "")),
            admission_date=str(data.get("admission_date", "")),
            status=str(data.get("status", "Active")),
            created_date=data.get("created_date"),
            updated_date=data.get("updated_date"),
            department_name=str(data.get("department_name", "")),
            department_code=str(data.get("department_code", "")),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes Student object to dictionary."""
        return {
            "id": self.id,
            "admission_number": self.admission_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "gender": self.gender,
            "date_of_birth": self.date_of_birth,
            "phone_number": self.phone_number,
            "email": self.email,
            "address": self.address,
            "department_id": self.department_id,
            "department_name": self.department_name,
            "year": self.year,
            "guardian_name": self.guardian_name,
            "guardian_phone": self.guardian_phone,
            "admission_date": self.admission_date,
            "status": self.status,
        }
