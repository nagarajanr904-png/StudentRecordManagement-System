"""
Services package containing business logic, validation, and data orchestration.
"""
from app.services.department_service import DepartmentService
from app.services.student_service import StudentService
from app.services.attendance_service import AttendanceService
from app.services.marks_service import MarksService
from app.services.report_service import ReportService

__all__ = [
    "DepartmentService",
    "StudentService",
    "AttendanceService",
    "MarksService",
    "ReportService",
]
