"""
Application screens package.
"""
from app.screens.dashboard import DashboardScreen
from app.screens.students import StudentsScreen
from app.screens.student_form import StudentFormScreen
from app.screens.student_details import StudentDetailsScreen
from app.screens.attendance import AttendanceScreen
from app.screens.marks import MarksScreen
from app.screens.departments import DepartmentsScreen
from app.screens.reports import ReportsScreen
from app.screens.settings_screen import SettingsScreen

__all__ = [
    "DashboardScreen",
    "StudentsScreen",
    "StudentFormScreen",
    "StudentDetailsScreen",
    "AttendanceScreen",
    "MarksScreen",
    "DepartmentsScreen",
    "ReportsScreen",
    "SettingsScreen",
]
