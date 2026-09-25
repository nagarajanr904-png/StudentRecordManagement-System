"""
Marks and academic evaluation service.
Handles score entries, grade calculation, GPA/percentage tracking, and validation.
"""

from typing import List, Optional, Tuple
from app.database.connection import get_db
from app.database import queries
from app.models.marks import Marks
from app.utils.helpers import calculate_grade
from app.utils.validators import validate_marks, validate_required
from app.config.settings import logger


class MarksService:
    """Service handling examination scores and transcript grades."""

    def __init__(self) -> None:
        self.db = get_db()

    def get_by_student(self, student_id: int) -> List[Marks]:
        """Retrieves all examination marks for a given student."""
        success, rows, _ = self.db.execute_query(queries.SELECT_MARKS_BY_STUDENT, (student_id,))
        if not success or not rows:
            return []
        return [Marks.from_dict(row) for row in rows]

    def get_all(self) -> List[Marks]:
        """Retrieves all exam marks across the institution."""
        success, rows, _ = self.db.execute_query(queries.SELECT_ALL_MARKS)
        if not success or not rows:
            return []
        return [Marks.from_dict(row) for row in rows]

    def record_marks(
        self,
        student_id: int,
        subject: str,
        exam_name: str,
        marks_obtained_str: str,
        max_marks_str: str = "100.00",
        remarks: str = "",
    ) -> Tuple[bool, str, Optional[int]]:
        """Validates, calculates percentage and grade, and records exam marks."""
        if not student_id or student_id <= 0:
            return False, "Please select a valid student.", None

        ok, msg = validate_required(subject, "Subject")
        if not ok:
            return False, msg, None

        ok, msg = validate_required(exam_name, "Exam name")
        if not ok:
            return False, msg, None

        valid_marks, err_m, obtained, max_m = validate_marks(marks_obtained_str, max_marks_str)
        if not valid_marks:
            return False, err_m, None

        percentage = round((obtained / max_m * 100), 2)
        grade = calculate_grade(percentage)

        params = (
            student_id,
            subject.strip(),
            exam_name.strip(),
            obtained,
            max_m,
            percentage,
            grade,
            remarks.strip() if remarks else "",
        )

        success, insert_id, err = self.db.execute_non_query(queries.INSERT_MARKS, params)
        if not success:
            return False, err or "Failed to record examination marks.", None

        logger.info("Recorded marks for student %s in %s (%s%%, Grade: %s)", student_id, subject, percentage, grade)
        return True, "Marks recorded successfully.", insert_id

    def update_marks(
        self,
        mark_id: int,
        student_id: int,
        subject: str,
        exam_name: str,
        marks_obtained_str: str,
        max_marks_str: str = "100.00",
        remarks: str = "",
    ) -> Tuple[bool, str]:
        """Updates an existing marks entry."""
        valid_marks, err_m, obtained, max_m = validate_marks(marks_obtained_str, max_marks_str)
        if not valid_marks:
            return False, err_m

        percentage = round((obtained / max_m * 100), 2)
        grade = calculate_grade(percentage)

        params = (
            student_id,
            subject.strip(),
            exam_name.strip(),
            obtained,
            max_m,
            percentage,
            grade,
            remarks.strip() if remarks else "",
            mark_id,
        )

        success, _, err = self.db.execute_non_query(queries.UPDATE_MARKS, params)
        if not success:
            return False, err or "Failed to update marks entry."

        return True, "Marks updated successfully."

    def delete_marks(self, mark_id: int) -> Tuple[bool, str]:
        """Deletes an examination marks entry."""
        success, _, err = self.db.execute_non_query(queries.DELETE_MARKS, (mark_id,))
        if not success:
            return False, err or "Failed to delete marks entry."
        return True, "Marks entry deleted."
