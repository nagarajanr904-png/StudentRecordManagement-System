"""
Student business service.
Orchestrates CRUD operations, complex searches, filters, validation, and dashboard metrics.
"""

from typing import Any, Dict, List, Optional, Tuple
from app.database.connection import get_db
from app.database import queries
from app.models.student import Student
from app.utils.validators import (
    validate_admission_number,
    validate_date,
    validate_email,
    validate_phone,
    validate_required,
    validate_academic_year,
)
from app.config.settings import logger


class StudentService:
    """Service handling all student record interactions."""

    def __init__(self) -> None:
        self.db = get_db()

    def get_all(self) -> List[Student]:
        """Retrieves all students ordered by newest first."""
        success, rows, _ = self.db.execute_query(queries.SELECT_ALL_STUDENTS)
        if not success or not rows:
            return []
        return [Student.from_dict(row) for row in rows]

    def get_by_id(self, student_id: int) -> Optional[Student]:
        """Retrieves single student by primary key."""
        success, row, _ = self.db.execute_query(queries.SELECT_STUDENT_BY_ID, (student_id,), fetch_one=True)
        if success and row:
            return Student.from_dict(row)
        return None

    def search(
        self,
        query_text: str = "",
        department_id: Optional[int] = None,
        status: Optional[str] = None,
        year: Optional[int] = None,
        gender: Optional[str] = None,
    ) -> List[Student]:
        """
        Multi-criteria student search and filtering:
        - Searches ID, admission number, full name, phone number, department name
        - Filters by department, status, year, and gender
        """
        clean_text = (query_text or "").strip()

        if clean_text:
            wildcard = f"%{clean_text}%"
            # Parameterized search across multiple indexed fields
            params = (wildcard, wildcard, wildcard, wildcard, wildcard, wildcard, clean_text)
            success, rows, _ = self.db.execute_query(queries.SEARCH_STUDENTS, params)
        else:
            success, rows, _ = self.db.execute_query(queries.SELECT_ALL_STUDENTS)

        if not success or not rows:
            return []

        students = [Student.from_dict(row) for row in rows]

        # Apply secondary filters if requested
        if department_id and department_id > 0:
            students = [s for s in students if s.department_id == department_id]

        if status and status != "All":
            students = [s for s in students if s.status.lower() == status.lower()]

        if year and year > 0:
            students = [s for s in students if s.year == year]

        if gender and gender != "All":
            students = [s for s in students if s.gender.lower() == gender.lower()]

        return students

    def validate_student_data(self, data: Dict[str, Any], is_update: bool = False, student_id: Optional[int] = None) -> Tuple[bool, str]:
        """Performs comprehensive validation for student input fields."""
        # 1. Admission Number
        ok, msg = validate_admission_number(data.get("admission_number"))
        if not ok:
            return False, msg

        # Check unique admission number
        adm_no = str(data.get("admission_number", "")).strip()
        succ, existing, _ = self.db.execute_query(queries.SELECT_STUDENT_BY_ADMISSION_NUMBER, (adm_no,), fetch_one=True)
        if succ and existing:
            if not is_update or (is_update and existing.get("id") != student_id):
                return False, f"Admission number '{adm_no}' is already assigned to {existing.get('first_name')} {existing.get('last_name')}."

        # 2. Names
        ok, msg = validate_required(data.get("first_name"), "First name")
        if not ok:
            return False, msg

        ok, msg = validate_required(data.get("last_name"), "Last name")
        if not ok:
            return False, msg

        # 3. Dates
        ok, msg = validate_date(data.get("date_of_birth"), "Date of birth")
        if not ok:
            return False, msg

        ok, msg = validate_date(data.get("admission_date"), "Admission date")
        if not ok:
            return False, msg

        # 4. Contacts
        ok, msg = validate_email(data.get("email"))
        if not ok:
            return False, msg

        ok, msg = validate_phone(data.get("phone_number"), "Student phone number")
        if not ok:
            return False, msg

        ok, msg = validate_required(data.get("address"), "Address")
        if not ok:
            return False, msg

        # 5. Department & Year
        dept_id = data.get("department_id")
        if not dept_id or int(dept_id) <= 0:
            return False, "Please select an academic department."

        ok, msg = validate_academic_year(data.get("year"))
        if not ok:
            return False, msg

        # 6. Guardian Details
        ok, msg = validate_required(data.get("guardian_name"), "Guardian name")
        if not ok:
            return False, msg

        ok, msg = validate_phone(data.get("guardian_phone"), "Guardian phone number")
        if not ok:
            return False, msg

        return True, ""

    def create(self, data: Dict[str, Any]) -> Tuple[bool, str, Optional[int]]:
        """Validates and registers a new student."""
        is_valid, error_msg = self.validate_student_data(data, is_update=False)
        if not is_valid:
            return False, error_msg, None

        params = (
            str(data["admission_number"]).strip(),
            str(data["first_name"]).strip(),
            str(data["last_name"]).strip(),
            str(data.get("gender", "Male")).strip(),
            str(data["date_of_birth"]).strip(),
            str(data["phone_number"]).strip(),
            str(data["email"]).strip().lower(),
            str(data["address"]).strip(),
            int(data["department_id"]),
            int(data.get("year", 1)),
            str(data["guardian_name"]).strip(),
            str(data["guardian_phone"]).strip(),
            str(data["admission_date"]).strip(),
            str(data.get("status", "Active")).strip(),
        )

        success, insert_id, err = self.db.execute_non_query(queries.INSERT_STUDENT, params)
        if not success:
            return False, err or "Failed to create student record.", None

        logger.info("Created new student: %s %s (ID: %s)", data['first_name'], data['last_name'], insert_id)
        return True, "Student record created successfully.", insert_id

    def update(self, student_id: int, data: Dict[str, Any]) -> Tuple[bool, str]:
        """Validates and updates an existing student."""
        is_valid, error_msg = self.validate_student_data(data, is_update=True, student_id=student_id)
        if not is_valid:
            return False, error_msg

        params = (
            str(data["admission_number"]).strip(),
            str(data["first_name"]).strip(),
            str(data["last_name"]).strip(),
            str(data.get("gender", "Male")).strip(),
            str(data["date_of_birth"]).strip(),
            str(data["phone_number"]).strip(),
            str(data["email"]).strip().lower(),
            str(data["address"]).strip(),
            int(data["department_id"]),
            int(data.get("year", 1)),
            str(data["guardian_name"]).strip(),
            str(data["guardian_phone"]).strip(),
            str(data["admission_date"]).strip(),
            str(data.get("status", "Active")).strip(),
            student_id,
        )

        success, _, err = self.db.execute_non_query(queries.UPDATE_STUDENT, params)
        if not success:
            return False, err or "Failed to update student record."

        logger.info("Updated student ID %s", student_id)
        return True, "Student record updated successfully."

    def set_status(self, student_id: int, status: str) -> Tuple[bool, str]:
        """Activates, deactivates, or changes status of student."""
        success, _, err = self.db.execute_non_query(queries.UPDATE_STUDENT_STATUS, (status, student_id))
        if not success:
            return False, err or f"Failed to change status to {status}."
        logger.info("Changed student %s status to %s", student_id, status)
        return True, f"Student status successfully updated to {status}."

    def delete(self, student_id: int) -> Tuple[bool, str]:
        """Deletes student record and cascades attendance and marks."""
        success, _, err = self.db.execute_non_query(queries.DELETE_STUDENT, (student_id,))
        if not success:
            return False, err or "Failed to delete student record."
        logger.info("Deleted student ID %s", student_id)
        return True, "Student record and associated records deleted successfully."

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        """Retrieves real-time dashboard counters and recent registrations."""
        success, row, _ = self.db.execute_query(queries.DASHBOARD_METRICS, fetch_one=True)
        metrics = {
            "total_students": 0,
            "active_students": 0,
            "male_students": 0,
            "female_students": 0,
            "total_departments": 0,
        }
        if success and row:
            metrics["total_students"] = int(row.get("total_students", 0))
            metrics["active_students"] = int(row.get("active_students", 0))
            metrics["male_students"] = int(row.get("male_students", 0))
            metrics["female_students"] = int(row.get("female_students", 0))
            metrics["total_departments"] = int(row.get("total_departments", 0))

        # Fetch recent students
        s_ok, recent_rows, _ = self.db.execute_query(queries.RECENT_STUDENTS)
        recent = [Student.from_dict(r) for r in recent_rows] if (s_ok and recent_rows) else []

        metrics["recent_students"] = recent
        return metrics
