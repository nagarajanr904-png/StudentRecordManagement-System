"""
Department entity model.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Department:
    """Represents an academic department or faculty."""

    id: Optional[int] = None
    code: str = ""
    name: str = ""
    description: str = ""
    status: str = "Active"
    created_at: Optional[Any] = None
    updated_at: Optional[Any] = None
    student_count: int = 0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Department":
        """Constructs a Department model from database dictionary."""
        return cls(
            id=data.get("id"),
            code=str(data.get("code", "")),
            name=str(data.get("name", "")),
            description=str(data.get("description", "") or ""),
            status=str(data.get("status", "Active")),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            student_count=int(data.get("student_count", 0)),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serializes Department to dictionary."""
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "student_count": self.student_count,
        }
