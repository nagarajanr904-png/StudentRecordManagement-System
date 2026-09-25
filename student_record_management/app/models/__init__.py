"""
Data models package.
"""
from app.models.department import Department
from app.models.student import Student
from app.models.attendance import Attendance
from app.models.marks import Marks

__all__ = ["Department", "Student", "Attendance", "Marks"]
