"""
Department business service.
Manages department creation, updates, validation, listing, and deletion integrity.
"""

from typing import List, Optional, Tuple
from app.database.connection import get_db
from app.database import queries
from app.models.department import Department
from app.utils.validators import validate_required
from app.config.settings import logger


class DepartmentService:
    """Service handling department operations."""

    def __init__(self) -> None:
        self.db = get_db()

    def get_all(self) -> List[Department]:
        """Retrieves all departments with student count."""
        success, rows, err = self.db.execute_query(queries.SELECT_ALL_DEPARTMENTS)
        if not success or not rows:
            return []
        return [Department.from_dict(row) for row in rows]

    def get_active(self) -> List[Department]:
        """Retrieves only currently active departments."""
        success, rows, err = self.db.execute_query(queries.SELECT_ACTIVE_DEPARTMENTS)
        if not success or not rows:
            return []
        return [Department.from_dict(row) for row in rows]

    def get_by_id(self, dept_id: int) -> Optional[Department]:
        """Retrieves single department by ID."""
        success, row, err = self.db.execute_query(queries.SELECT_DEPARTMENT_BY_ID, (dept_id,), fetch_one=True)
        if success and row:
            return Department.from_dict(row)
        return None

    def create(self, code: str, name: str, description: str = "", status: str = "Active") -> Tuple[bool, str, Optional[int]]:
        """Validates and creates a new department."""
        ok, msg = validate_required(code, "Department code")
        if not ok:
            return False, msg, None

        ok, msg = validate_required(name, "Department name")
        if not ok:
            return False, msg, None

        params = (code.strip().upper(), name.strip(), description.strip(), status.strip())
        success, insert_id, err_msg = self.db.execute_non_query(queries.INSERT_DEPARTMENT, params)

        if not success:
            return False, err_msg or "Failed to create department.", None

        logger.info("Created department '%s' (ID: %s)", name, insert_id)
        return True, "Department created successfully.", insert_id

    def update(self, dept_id: int, code: str, name: str, description: str, status: str) -> Tuple[bool, str]:
        """Validates and updates existing department."""
        ok, msg = validate_required(code, "Department code")
        if not ok:
            return False, msg

        ok, msg = validate_required(name, "Department name")
        if not ok:
            return False, msg

        params = (code.strip().upper(), name.strip(), description.strip(), status.strip(), dept_id)
        success, _, err_msg = self.db.execute_non_query(queries.UPDATE_DEPARTMENT, params)

        if not success:
            return False, err_msg or "Failed to update department."

        logger.info("Updated department ID %s", dept_id)
        return True, "Department updated successfully."

    def delete(self, dept_id: int) -> Tuple[bool, str]:
        """Deletes department if no students are currently enrolled in it."""
        # Check student reference constraint
        ok, res, _ = self.db.execute_query(queries.CHECK_DEPARTMENT_STUDENTS, (dept_id,), fetch_one=True)
        if ok and res and res.get("count", 0) > 0:
            count = res.get("count")
            return False, f"Cannot delete department. There are {count} student(s) currently enrolled in it."

        success, _, err_msg = self.db.execute_non_query(queries.DELETE_DEPARTMENT, (dept_id,))
        if not success:
            return False, err_msg or "Failed to delete department."

        logger.info("Deleted department ID %s", dept_id)
        return True, "Department deleted successfully."
