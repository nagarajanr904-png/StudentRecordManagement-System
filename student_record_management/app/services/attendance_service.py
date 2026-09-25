"""
Attendance business service.
Handles daily student roll call, bulk attendance marking, history auditing,
and student attendance summary calculation.
"""

from typing import Any, Dict, List, Optional, Tuple
from app.database.connection import get_db
from app.database import queries
from app.models.attendance import Attendance
from app.utils.validators import validate_date
from app.config.settings import logger


class AttendanceService:
    """Service handling attendance records and analytics."""

    def __init__(self) -> None:
        self.db = get_db()

    def get_by_date(self, target_date: str) -> List[Attendance]:
        """Retrieves attendance entries for a specific calendar date."""
        success, rows, _ = self.db.execute_query(queries.SELECT_ATTENDANCE_BY_DATE, (target_date,))
        if not success or not rows:
            return []
        return [Attendance.from_dict(row) for row in rows]

    def get_by_student(self, student_id: int) -> List[Attendance]:
        """Retrieves attendance history for an individual student."""
        success, rows, _ = self.db.execute_query(queries.SELECT_ATTENDANCE_BY_STUDENT, (student_id,))
        if not success or not rows:
            return []
        return [Attendance.from_dict(row) for row in rows]

    def get_summary_for_student(self, student_id: int) -> Dict[str, Any]:
        """Computes total records, attendance percentage, present, absent, and late counts."""
        success, row, _ = self.db.execute_query(queries.SELECT_STUDENT_ATTENDANCE_SUMMARY, (student_id,), fetch_one=True)
        summary = {
            "total": 0,
            "present": 0,
            "absent": 0,
            "late": 0,
            "percentage": 0.0,
        }
        if success and row:
            total = int(row.get("total_recorded", 0) or 0)
            present = int(row.get("present_count", 0) or 0)
            absent = int(row.get("absent_count", 0) or 0)
            late = int(row.get("late_count", 0) or 0)

            percentage = round((present / total * 100), 1) if total > 0 else 0.0

            summary["total"] = total
            summary["present"] = present
            summary["absent"] = absent
            summary["late"] = late
            summary["percentage"] = percentage

        return summary

    def mark_attendance(
        self, student_id: int, attendance_date: str, status: str, remarks: Optional[str] = None
    ) -> Tuple[bool, str]:
        """Creates or updates attendance entry for a student on a specific date."""
        ok, msg = validate_date(attendance_date, "Attendance date")
        if not ok:
            return False, msg

        clean_status = status.capitalize()
        if clean_status not in ("Present", "Absent", "Late"):
            clean_status = "Present"

        clean_remarks = remarks.strip() if remarks else ""

        params = (student_id, attendance_date, clean_status, clean_remarks)
        success, _, err = self.db.execute_non_query(queries.UPSERT_ATTENDANCE, params)

        if not success:
            return False, err or "Failed to record attendance."

        return True, "Attendance marked successfully."

    def bulk_mark_present(self, student_ids: List[int], attendance_date: str) -> Tuple[int, int]:
        """Convenience method to quickly mark multiple students present for a day."""
        success_count = 0
        fail_count = 0
        for sid in student_ids:
            ok, _ = self.mark_attendance(sid, attendance_date, "Present", "On time")
            if ok:
                success_count += 1
            else:
                fail_count += 1
        return success_count, fail_count

    def delete_record(self, record_id: int) -> Tuple[bool, str]:
        """Deletes an attendance entry."""
        success, _, err = self.db.execute_non_query(queries.DELETE_ATTENDANCE, (record_id,))
        if not success:
            return False, err or "Failed to delete attendance record."
        return True, "Attendance entry deleted."
