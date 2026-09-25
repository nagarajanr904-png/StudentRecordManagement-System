"""
Database connection and query execution layer.
Handles MySQL connections, pooling, parameterized execution, transactions,
and provides graceful fallback with user-friendly error messages.
"""

import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime

from app.config.settings import Settings, logger, BASE_DIR

# Attempt to import mysql.connector safely
try:
    import mysql.connector
    from mysql.connector import Error as MySQLError, pooling
    MYSQL_CONNECTOR_AVAILABLE = True
except ImportError:
    MYSQL_CONNECTOR_AVAILABLE = False
    MySQLError = Exception  # type: ignore


class DatabaseConnection:
    """
    Singleton database manager.
    Coordinates connection pools, parameterized queries, transaction commits/rollbacks,
    and automatic fallback to memory store if remote MySQL credentials are not set.
    """

    _instance: Optional["DatabaseConnection"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "DatabaseConnection":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseConnection, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return

        self._pool: Optional[Any] = None
        self._is_connected: bool = False
        self._last_error: Optional[str] = None
        self._using_mock_fallback: bool = False
        self._mock_data: Dict[str, List[Dict[str, Any]]] = {}

        self._init_mock_store()
        self.connect()
        self._initialized = True

    def _init_mock_store(self) -> None:
        """Initializes high-fidelity sample data for offline testing/evaluation."""
        self._mock_data = {
            "departments": [
                {
                    "id": 1,
                    "code": "CS",
                    "name": "Computer Science & Engineering",
                    "description": "Undergraduate program covering software engineering, algorithms, and AI.",
                    "status": "Active",
                    "created_at": datetime(2023, 1, 15, 10, 0),
                    "updated_at": datetime(2023, 1, 15, 10, 0),
                },
                {
                    "id": 2,
                    "code": "EE",
                    "name": "Electrical & Electronics Engineering",
                    "description": "Circuit theory, digital systems, power electronics, and telecom.",
                    "status": "Active",
                    "created_at": datetime(2023, 1, 15, 10, 0),
                    "updated_at": datetime(2023, 1, 15, 10, 0),
                },
                {
                    "id": 3,
                    "code": "ME",
                    "name": "Mechanical Engineering",
                    "description": "Thermodynamics, CAD design, robotics, and applied mechanics.",
                    "status": "Active",
                    "created_at": datetime(2023, 1, 15, 10, 0),
                    "updated_at": datetime(2023, 1, 15, 10, 0),
                },
                {
                    "id": 4,
                    "code": "BA",
                    "name": "Business Administration",
                    "description": "Organizational leadership, business analytics, and marketing management.",
                    "status": "Active",
                    "created_at": datetime(2023, 1, 15, 10, 0),
                    "updated_at": datetime(2023, 1, 15, 10, 0),
                },
            ],
            "students": [
                {
                    "id": 1,
                    "admission_number": "ADM-2023-001",
                    "first_name": "Alexander",
                    "last_name": "Wright",
                    "gender": "Male",
                    "date_of_birth": "2004-03-15",
                    "phone_number": "+1-555-0101",
                    "email": "a.wright@example.com",
                    "address": "742 Evergreen Terrace, Springfield, OR",
                    "department_id": 1,
                    "year": 2,
                    "guardian_name": "Robert Wright",
                    "guardian_phone": "+1-555-9101",
                    "admission_date": "2023-08-20",
                    "status": "Active",
                    "created_date": datetime(2023, 8, 20, 9, 30),
                    "updated_date": datetime(2023, 8, 20, 9, 30),
                },
                {
                    "id": 2,
                    "admission_number": "ADM-2023-002",
                    "first_name": "Sophia",
                    "last_name": "Chen",
                    "gender": "Female",
                    "date_of_birth": "2004-07-22",
                    "phone_number": "+1-555-0102",
                    "email": "s.chen@example.com",
                    "address": "124 Conch Street, Pacific Grove, CA",
                    "department_id": 1,
                    "year": 2,
                    "guardian_name": "David Chen",
                    "guardian_phone": "+1-555-9102",
                    "admission_date": "2023-08-20",
                    "status": "Active",
                    "created_date": datetime(2023, 8, 20, 9, 45),
                    "updated_date": datetime(2023, 8, 20, 9, 45),
                },
                {
                    "id": 3,
                    "admission_number": "ADM-2022-045",
                    "first_name": "Marcus",
                    "last_name": "Johnson",
                    "gender": "Male",
                    "date_of_birth": "2003-11-09",
                    "phone_number": "+1-555-0103",
                    "email": "m.johnson@example.com",
                    "address": "884 Elm Avenue, Seattle, WA",
                    "department_id": 2,
                    "year": 3,
                    "guardian_name": "Patricia Johnson",
                    "guardian_phone": "+1-555-9103",
                    "admission_date": "2022-08-15",
                    "status": "Active",
                    "created_date": datetime(2022, 8, 15, 11, 0),
                    "updated_date": datetime(2022, 8, 15, 11, 0),
                },
                {
                    "id": 4,
                    "admission_number": "ADM-2024-101",
                    "first_name": "Elena",
                    "last_name": "Rodriguez",
                    "gender": "Female",
                    "date_of_birth": "2005-01-30",
                    "phone_number": "+1-555-0104",
                    "email": "e.rodriguez@example.com",
                    "address": "312 Maple Drive, Austin, TX",
                    "department_id": 1,
                    "year": 1,
                    "guardian_name": "Carlos Rodriguez",
                    "guardian_phone": "+1-555-9104",
                    "admission_date": "2024-08-22",
                    "status": "Active",
                    "created_date": datetime(2024, 8, 22, 10, 15),
                    "updated_date": datetime(2024, 8, 22, 10, 15),
                },
                {
                    "id": 5,
                    "admission_number": "ADM-2022-089",
                    "first_name": "Liam",
                    "last_name": "O'Connor",
                    "gender": "Male",
                    "date_of_birth": "2003-05-18",
                    "phone_number": "+1-555-0105",
                    "email": "l.oconnor@example.com",
                    "address": "56 Pine Street, Boston, MA",
                    "department_id": 3,
                    "year": 3,
                    "guardian_name": "Fiona O'Connor",
                    "guardian_phone": "+1-555-9105",
                    "admission_date": "2022-08-15",
                    "status": "Active",
                    "created_date": datetime(2022, 8, 15, 14, 0),
                    "updated_date": datetime(2022, 8, 15, 14, 0),
                },
                {
                    "id": 6,
                    "admission_number": "ADM-2024-118",
                    "first_name": "Amina",
                    "last_name": "Patel",
                    "gender": "Female",
                    "date_of_birth": "2005-09-12",
                    "phone_number": "+1-555-0106",
                    "email": "a.patel@example.com",
                    "address": "901 Cedar Boulevard, Denver, CO",
                    "department_id": 4,
                    "year": 1,
                    "guardian_name": "Suresh Patel",
                    "guardian_phone": "+1-555-9106",
                    "admission_date": "2024-08-22",
                    "status": "Active",
                    "created_date": datetime(2024, 8, 22, 11, 30),
                    "updated_date": datetime(2024, 8, 22, 11, 30),
                },
                {
                    "id": 7,
                    "admission_number": "ADM-2021-012",
                    "first_name": "Ethan",
                    "last_name": "Miller",
                    "gender": "Male",
                    "date_of_birth": "2002-12-04",
                    "phone_number": "+1-555-0107",
                    "email": "e.miller@example.com",
                    "address": "440 Birch Lane, Minneapolis, MN",
                    "department_id": 3,
                    "year": 4,
                    "guardian_name": "Sarah Miller",
                    "guardian_phone": "+1-555-9107",
                    "admission_date": "2021-08-18",
                    "status": "Active",
                    "created_date": datetime(2021, 8, 18, 9, 0),
                    "updated_date": datetime(2021, 8, 18, 9, 0),
                },
                {
                    "id": 8,
                    "admission_number": "ADM-2023-055",
                    "first_name": "Chloe",
                    "last_name": "Dubois",
                    "gender": "Female",
                    "date_of_birth": "2004-04-28",
                    "phone_number": "+1-555-0108",
                    "email": "c.dubois@example.com",
                    "address": "710 Oak Ridge Road, Atlanta, GA",
                    "department_id": 4,
                    "year": 2,
                    "guardian_name": "Henri Dubois",
                    "guardian_phone": "+1-555-9108",
                    "admission_date": "2023-08-20",
                    "status": "Active",
                    "created_date": datetime(2023, 8, 20, 15, 20),
                    "updated_date": datetime(2023, 8, 20, 15, 20),
                },
                {
                    "id": 9,
                    "admission_number": "ADM-2022-130",
                    "first_name": "Lucas",
                    "last_name": "Silva",
                    "gender": "Male",
                    "date_of_birth": "2003-08-14",
                    "phone_number": "+1-555-0109",
                    "email": "l.silva@example.com",
                    "address": "225 Willow Way, Miami, FL",
                    "department_id": 2,
                    "year": 3,
                    "guardian_name": "Isabella Silva",
                    "guardian_phone": "+1-555-9109",
                    "admission_date": "2022-08-15",
                    "status": "Active",
                    "created_date": datetime(2022, 8, 15, 16, 0),
                    "updated_date": datetime(2022, 8, 15, 16, 0),
                },
                {
                    "id": 10,
                    "admission_number": "ADM-2024-142",
                    "first_name": "Zoe",
                    "last_name": "Kowalski",
                    "gender": "Female",
                    "date_of_birth": "2005-06-03",
                    "phone_number": "+1-555-0110",
                    "email": "z.kowalski@example.com",
                    "address": "180 Walnut Court, Chicago, IL",
                    "department_id": 1,
                    "year": 1,
                    "guardian_name": "Jan Kowalski",
                    "guardian_phone": "+1-555-9110",
                    "admission_date": "2024-08-22",
                    "status": "Active",
                    "created_date": datetime(2024, 8, 22, 13, 40),
                    "updated_date": datetime(2024, 8, 22, 13, 40),
                },
            ],
            "attendance": [
                {"id": 1, "student_id": 1, "attendance_date": "2026-09-21", "status": "Present", "remarks": "On time"},
                {"id": 2, "student_id": 2, "attendance_date": "2026-09-21", "status": "Present", "remarks": "On time"},
                {"id": 3, "student_id": 3, "attendance_date": "2026-09-21", "status": "Present", "remarks": "On time"},
                {"id": 4, "student_id": 4, "attendance_date": "2026-09-21", "status": "Late", "remarks": "Bus traffic"},
                {"id": 5, "student_id": 5, "attendance_date": "2026-09-21", "status": "Present", "remarks": "On time"},
                {"id": 6, "student_id": 6, "attendance_date": "2026-09-21", "status": "Absent", "remarks": "Medical leave"},
                {"id": 7, "student_id": 1, "attendance_date": "2026-09-22", "status": "Present", "remarks": "On time"},
                {"id": 8, "student_id": 2, "attendance_date": "2026-09-22", "status": "Present", "remarks": "On time"},
                {"id": 9, "student_id": 3, "attendance_date": "2026-09-22", "status": "Late", "remarks": "Transit delay"},
                {"id": 10, "student_id": 4, "attendance_date": "2026-09-22", "status": "Present", "remarks": "On time"},
            ],
            "marks": [
                {
                    "id": 1,
                    "student_id": 1,
                    "subject": "Data Structures & Algorithms",
                    "exam_name": "Sem Exam",
                    "marks_obtained": 92.50,
                    "max_marks": 100.00,
                    "percentage": 92.50,
                    "grade": "A+",
                    "remarks": "Outstanding code implementation",
                },
                {
                    "id": 2,
                    "student_id": 1,
                    "subject": "Database Systems",
                    "exam_name": "Sem Exam",
                    "marks_obtained": 88.00,
                    "max_marks": 100.00,
                    "percentage": 88.00,
                    "grade": "A",
                    "remarks": "Strong SQL knowledge",
                },
                {
                    "id": 3,
                    "student_id": 2,
                    "subject": "Data Structures & Algorithms",
                    "exam_name": "Sem Exam",
                    "marks_obtained": 95.00,
                    "max_marks": 100.00,
                    "percentage": 95.00,
                    "grade": "A+",
                    "remarks": "Top score in cohort",
                },
                {
                    "id": 4,
                    "student_id": 3,
                    "subject": "Digital Signal Processing",
                    "exam_name": "Sem Exam",
                    "marks_obtained": 78.50,
                    "max_marks": 100.00,
                    "percentage": 78.50,
                    "grade": "B",
                    "remarks": "Good theoretical understanding",
                },
                {
                    "id": 5,
                    "student_id": 4,
                    "subject": "Introduction to Programming",
                    "exam_name": "Quiz 1",
                    "marks_obtained": 94.00,
                    "max_marks": 100.00,
                    "percentage": 94.00,
                    "grade": "A+",
                    "remarks": "Excellent syntax and logic",
                },
            ],
        }

    def connect(self) -> Tuple[bool, str]:
        """
        Attempts connection to MySQL using parameters loaded from .env.
        If credentials are absent or remote host is unreachable, activates offline
        safe mode so the application starts cleanly with informative messaging.
        """
        Settings.reload_env()

        if not Settings.is_db_configured():
            msg = (
                "MySQL credentials not detected in .env. Running in Local Offline Demonstration Mode. "
                "Configure your remote MySQL host in .env to connect to live cloud database."
            )
            logger.info(msg)
            self._using_mock_fallback = True
            self._is_connected = False
            self._last_error = msg
            return False, msg

        if not MYSQL_CONNECTOR_AVAILABLE:
            msg = "mysql-connector-python package is not installed. Please run: pip install -r requirements.txt"
            logger.warning(msg)
            self._using_mock_fallback = True
            self._is_connected = False
            self._last_error = msg
            return False, msg

        try:
            logger.info("Attempting connection to MySQL server at %s:%s...", Settings.DB_HOST, Settings.DB_PORT)
            self._pool = pooling.MySQLConnectionPool(
                pool_name=Settings.DB_POOL_NAME,
                pool_size=min(Settings.DB_POOL_SIZE, 5),
                pool_reset_session=True,
                host=Settings.DB_HOST,
                port=Settings.DB_PORT,
                database=Settings.DB_NAME,
                user=Settings.DB_USER,
                password=Settings.DB_PASSWORD,
                connection_timeout=Settings.DB_CONNECT_TIMEOUT,
                autocommit=False,
            )

            # Test acquire and ping
            conn = self._pool.get_connection()
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT 1;")
                cursor.fetchone()

                # Check if schema exists on remote online MySQL; auto-provision if needed
                try:
                    cursor.execute("SHOW TABLES LIKE 'students';")
                    if not cursor.fetchone():
                        logger.info("Tables not detected in remote MySQL. Auto-provisioning database tables...")
                        self._auto_init_schema(cursor)
                except Exception as ex:
                    logger.warning("Remote schema check notice: %s", ex)

                cursor.close()
                conn.close()

                self._is_connected = True
                self._using_mock_fallback = False
                self._last_error = None
                success_msg = f"Successfully connected to MySQL database '{Settings.DB_NAME}' on {Settings.DB_HOST}."
                logger.info(success_msg)
                return True, success_msg

            return False, "Failed to establish active MySQL session."

        except Exception as e:
            error_message = (
                "Unable to connect to the database. Please check your internet connection or database settings."
            )
            # Log technical detail safely without exposing credentials
            logger.error("Database connection failure: %s (Type: %s)", str(e), type(e).__name__)
            self._is_connected = False
            self._using_mock_fallback = True
            self._last_error = error_message
            return False, error_message

    def _auto_init_schema(self, cursor: Any) -> None:
        """
        Automatically executes database/schema.sql and database/seed.sql
        directly on the free online MySQL instance if tables are missing.
        Eliminates the requirement for MySQL Workbench or any desktop tool.
        """
        try:
            schema_file = BASE_DIR / "database" / "schema.sql"
            if schema_file.exists():
                with open(schema_file, "r", encoding="utf-8") as f:
                    content = f.read()
                statements = [s.strip() for s in content.split(";") if s.strip()]
                for s in statements:
                    try:
                        cursor.execute(s)
                    except Exception as err:
                        if "already exists" not in str(err).lower():
                            logger.debug("Schema execute note: %s", err)
                logger.info("Successfully provisioned schema tables on remote MySQL.")

            seed_file = BASE_DIR / "database" / "seed.sql"
            if seed_file.exists():
                with open(seed_file, "r", encoding="utf-8") as f:
                    seed_content = f.read()
                seed_stmts = [s.strip() for s in seed_content.split(";") if s.strip()]
                for s in seed_stmts:
                    try:
                        cursor.execute(s)
                    except Exception as err:
                        if "duplicate" not in str(err).lower():
                            logger.debug("Seed execute note: %s", err)
                logger.info("Successfully populated seed records on remote MySQL.")
        except Exception as e:
            logger.warning("Auto-init schema notice: %s", e)

    def is_connected(self) -> bool:
        """Returns True if live MySQL connection pool is active."""
        return self._is_connected

    def is_mock_mode(self) -> bool:
        """Returns True if currently operating in offline/mock demo mode."""
        return self._using_mock_fallback

    def get_last_error(self) -> Optional[str]:
        """Returns the most recent user-facing error message."""
        return self._last_error

    def execute_query(
        self, query: str, params: Optional[Union[tuple, list]] = None, fetch_one: bool = False
    ) -> Tuple[bool, Union[List[Dict[str, Any]], Dict[str, Any], None], str]:
        """
        Executes a SELECT query using parameterized arguments.
        Returns (success: bool, data, error_message: str).
        """
        params = params or ()

        if self._using_mock_fallback or not self._is_connected:
            return self._mock_execute_query(query, params, fetch_one)

        conn = None
        cursor = None
        try:
            conn = self._pool.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params)
            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            return True, result, ""
        except MySQLError as err:
            logger.error("MySQL query error: %s (Code: %s)", getattr(err, "msg", str(err)), getattr(err, "errno", "N/A"))
            return False, None, "Database query failed. Please verify connection and retry."
        except Exception as ex:
            logger.error("Unexpected exception during query execution: %s", str(ex))
            return False, None, "An unexpected error occurred while querying the database."
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def execute_non_query(
        self, query: str, params: Optional[Union[tuple, list]] = None
    ) -> Tuple[bool, int, str]:
        """
        Executes an INSERT, UPDATE, or DELETE query with transaction safety.
        Automatically commits on success or rolls back on exception.
        Returns (success: bool, last_insert_id_or_affected_rows: int, error_message: str).
        """
        params = params or ()

        if self._using_mock_fallback or not self._is_connected:
            return self._mock_execute_non_query(query, params)

        conn = None
        cursor = None
        try:
            conn = self._pool.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            last_id = cursor.lastrowid or cursor.rowcount
            return True, last_id, ""
        except MySQLError as err:
            if conn:
                conn.rollback()
            msg = getattr(err, "msg", str(err))
            errno = getattr(err, "errno", None)
            logger.error("MySQL transaction rolled back. Error: %s (Errno: %s)", msg, errno)
            if errno == 1062:
                return False, 0, "Duplicate entry detected. Admission number or email must be unique."
            if errno == 1452:
                return False, 0, "Referenced record does not exist. Please check foreign keys."
            if errno == 1451:
                return False, 0, "Cannot delete record because it is referenced by existing students."
            return False, 0, "Unable to save record to database. Operation rolled back."
        except Exception as ex:
            if conn:
                conn.rollback()
            logger.error("Unexpected error during database commit: %s", str(ex))
            return False, 0, "An unexpected error occurred. Changes were not saved."
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    # ==========================================================================
    # In-memory Demonstration Engine (Allows immediate full evaluation)
    # ==========================================================================
    def _mock_execute_query(
        self, query: str, params: Union[tuple, list], fetch_one: bool
    ) -> Tuple[bool, Any, str]:
        """Handles mock in-memory queries for offline demonstration mode."""
        q_upper = query.strip().upper()

        # Dashboard metrics query
        if "DASHBOARD_METRICS" in query or ("TOTAL_STUDENTS" in q_upper and "MALE_STUDENTS" in q_upper):
            students = self._mock_data.get("students", [])
            departments = self._mock_data.get("departments", [])
            total_students = len(students)
            active_students = len([s for s in students if s.get("status") == "Active"])
            male_students = len([s for s in students if s.get("gender") == "Male"])
            female_students = len([s for s in students if s.get("gender") == "Female"])
            total_departments = len([d for d in departments if d.get("status") == "Active"])

            metric = {
                "total_students": total_students,
                "active_students": active_students,
                "male_students": male_students,
                "female_students": female_students,
                "total_departments": total_departments,
            }
            return True, (metric if fetch_one else [metric]), ""

        # Recent students query
        if "LIMIT 5" in q_upper and "FROM STUDENTS" in q_upper:
            students = sorted(self._mock_data.get("students", []), key=lambda s: s["id"], reverse=True)[:5]
            enriched = self._enrich_students(students)
            return True, enriched, ""

        # Select all departments with count
        if "FROM DEPARTMENTS" in q_upper and "SELECT_ALL_DEPARTMENTS" in query:
            depts = sorted(self._mock_data.get("departments", []), key=lambda d: d["name"])
            results = []
            for d in depts:
                st_count = len([s for s in self._mock_data.get("students", []) if s.get("department_id") == d["id"]])
                d_copy = dict(d)
                d_copy["student_count"] = st_count
                results.append(d_copy)
            return True, results, ""

        # Select active departments
        if "FROM DEPARTMENTS" in q_upper and "STATUS = 'ACTIVE'" in q_upper:
            active_depts = [d for d in self._mock_data.get("departments", []) if d.get("status") == "Active"]
            return True, sorted(active_depts, key=lambda d: d["name"]), ""

        # Select department by id
        if "FROM DEPARTMENTS" in q_upper and "WHERE ID = %S" in q_upper:
            dept_id = int(params[0]) if params else 0
            for d in self._mock_data.get("departments", []):
                if d["id"] == dept_id:
                    return True, (dict(d) if fetch_one else [dict(d)]), ""
            return True, (None if fetch_one else []), ""

        # Check department students count
        if "SELECT COUNT(*) AS COUNT FROM STUDENTS WHERE DEPARTMENT_ID = %S" in q_upper:
            dept_id = int(params[0]) if params else 0
            cnt = len([s for s in self._mock_data.get("students", []) if s.get("department_id") == dept_id])
            res = {"count": cnt}
            return True, (res if fetch_one else [res]), ""

        # Select all students
        if "FROM STUDENTS S" in q_upper and "WHERE S.ID = %S" not in q_upper and "SEARCH" not in query:
            all_st = sorted(self._mock_data.get("students", []), key=lambda s: s["id"], reverse=True)
            enriched = self._enrich_students(all_st)
            return True, enriched, ""

        # Select student by id
        if "FROM STUDENTS S" in q_upper and "WHERE S.ID = %S" in q_upper:
            st_id = int(params[0]) if params else 0
            for s in self._mock_data.get("students", []):
                if s["id"] == st_id:
                    enr = self._enrich_students([s])[0]
                    return True, (enr if fetch_one else [enr]), ""
            return True, (None if fetch_one else []), ""

        # Search students
        if "SEARCH_STUDENTS" in query or "LOWER(S.ADMISSION_NUMBER) LIKE" in q_upper:
            term = str(params[0]).replace("%", "").strip().lower() if params else ""
            matches = []
            for s in self._mock_data.get("students", []):
                full_name = f"{s.get('first_name', '')} {s.get('last_name', '')}".lower()
                adm = str(s.get("admission_number", "")).lower()
                phone = str(s.get("phone_number", "")).lower()
                st_id_str = str(s.get("id", ""))
                dept_name = self._get_dept_name(s.get("department_id")).lower()

                if (
                    not term
                    or term in adm
                    or term in full_name
                    or term in phone
                    or term in dept_name
                    or term == st_id_str
                ):
                    matches.append(s)
            enriched = self._enrich_students(sorted(matches, key=lambda x: x["id"], reverse=True))
            return True, enriched, ""

        # Check duplicate admission number
        if "SELECT ID, ADMISSION_NUMBER" in q_upper and "FROM STUDENTS" in q_upper:
            adm_val = str(params[0]).strip().lower() if params else ""
            for s in self._mock_data.get("students", []):
                if str(s.get("admission_number", "")).strip().lower() == adm_val:
                    return True, (s if fetch_one else [s]), ""
            return True, (None if fetch_one else []), ""

        # Attendance by date
        if "FROM ATTENDANCE A" in q_upper and "A.ATTENDANCE_DATE = %S" in q_upper:
            req_date = str(params[0]) if params else ""
            att_records = [a for a in self._mock_data.get("attendance", []) if str(a.get("attendance_date")) == req_date]
            enriched_att = []
            for a in att_records:
                st = next((s for s in self._mock_data.get("students", []) if s["id"] == a["student_id"]), None)
                if st:
                    item = dict(a)
                    item["admission_number"] = st.get("admission_number")
                    item["first_name"] = st.get("first_name")
                    item["last_name"] = st.get("last_name")
                    item["year"] = st.get("year")
                    item["department_name"] = self._get_dept_name(st.get("department_id"))
                    enriched_att.append(item)
            return True, enriched_att, ""

        # Attendance by student
        if "FROM ATTENDANCE" in q_upper and "WHERE STUDENT_ID = %S" in q_upper and "COUNT(*)" not in q_upper:
            st_id = int(params[0]) if params else 0
            records = [a for a in self._mock_data.get("attendance", []) if a["student_id"] == st_id]
            return True, sorted(records, key=lambda a: a.get("attendance_date", ""), reverse=True), ""

        # Student attendance summary
        if "FROM ATTENDANCE" in q_upper and "TOTAL_RECORDED" in q_upper:
            st_id = int(params[0]) if params else 0
            records = [a for a in self._mock_data.get("attendance", []) if a["student_id"] == st_id]
            tot = len(records)
            pres = len([a for a in records if a.get("status") == "Present"])
            ab = len([a for a in records if a.get("status") == "Absent"])
            late = len([a for a in records if a.get("status") == "Late"])
            summary = {
                "total_recorded": tot,
                "present_count": pres,
                "absent_count": ab,
                "late_count": late,
            }
            return True, (summary if fetch_one else [summary]), ""

        # Marks by student
        if "FROM MARKS" in q_upper and "WHERE STUDENT_ID = %S" in q_upper:
            st_id = int(params[0]) if params else 0
            records = [m for m in self._mock_data.get("marks", []) if m["student_id"] == st_id]
            return True, sorted(records, key=lambda m: (m.get("exam_name", ""), m.get("subject", ""))), ""

        # All marks
        if "FROM MARKS M" in q_upper:
            all_m = list(self._mock_data.get("marks", []))
            enriched_m = []
            for m in all_m:
                st = next((s for s in self._mock_data.get("students", []) if s["id"] == m["student_id"]), None)
                item = dict(m)
                if st:
                    item["admission_number"] = st.get("admission_number")
                    item["first_name"] = st.get("first_name")
                    item["last_name"] = st.get("last_name")
                    item["department_name"] = self._get_dept_name(st.get("department_id"))
                else:
                    item["admission_number"] = "N/A"
                    item["first_name"] = "Unknown"
                    item["last_name"] = ""
                    item["department_name"] = "N/A"
                enriched_m.append(item)
            return True, sorted(enriched_m, key=lambda x: x["id"], reverse=True), ""

        return True, ([] if not fetch_one else None), ""

    def _mock_execute_non_query(
        self, query: str, params: Union[tuple, list]
    ) -> Tuple[bool, int, str]:
        """Handles mock in-memory inserts, updates, and deletes."""
        q_upper = query.strip().upper()

        # Insert student
        if "INSERT INTO STUDENTS" in q_upper:
            adm_num = params[0]
            # Check duplicate admission
            for s in self._mock_data["students"]:
                if s["admission_number"].lower() == adm_num.lower():
                    return False, 0, f"Admission number '{adm_num}' is already assigned."

            new_id = max([s["id"] for s in self._mock_data["students"]] or [0]) + 1
            new_student = {
                "id": new_id,
                "admission_number": params[0],
                "first_name": params[1],
                "last_name": params[2],
                "gender": params[3],
                "date_of_birth": params[4],
                "phone_number": params[5],
                "email": params[6],
                "address": params[7],
                "department_id": int(params[8]),
                "year": int(params[9]),
                "guardian_name": params[10],
                "guardian_phone": params[11],
                "admission_date": params[12],
                "status": params[13],
                "created_date": datetime.now(),
                "updated_date": datetime.now(),
            }
            self._mock_data["students"].append(new_student)
            return True, new_id, ""

        # Update student
        if "UPDATE STUDENTS" in q_upper and "STATUS = %S" not in q_upper:
            st_id = int(params[14])
            for idx, s in enumerate(self._mock_data["students"]):
                if s["id"] == st_id:
                    s["admission_number"] = params[0]
                    s["first_name"] = params[1]
                    s["last_name"] = params[2]
                    s["gender"] = params[3]
                    s["date_of_birth"] = params[4]
                    s["phone_number"] = params[5]
                    s["email"] = params[6]
                    s["address"] = params[7]
                    s["department_id"] = int(params[8])
                    s["year"] = int(params[9])
                    s["guardian_name"] = params[10]
                    s["guardian_phone"] = params[11]
                    s["admission_date"] = params[12]
                    s["status"] = params[13]
                    s["updated_date"] = datetime.now()
                    return True, 1, ""
            return False, 0, "Student record not found."

        # Update student status
        if "UPDATE STUDENTS" in q_upper and "SET STATUS = %S" in q_upper:
            new_status = params[0]
            st_id = int(params[1])
            for s in self._mock_data["students"]:
                if s["id"] == st_id:
                    s["status"] = new_status
                    s["updated_date"] = datetime.now()
                    return True, 1, ""
            return False, 0, "Student record not found."

        # Delete student
        if "DELETE FROM STUDENTS" in q_upper:
            st_id = int(params[0])
            initial_len = len(self._mock_data["students"])
            self._mock_data["students"] = [s for s in self._mock_data["students"] if s["id"] != st_id]
            # Cascade in mock
            self._mock_data["attendance"] = [a for a in self._mock_data["attendance"] if a["student_id"] != st_id]
            self._mock_data["marks"] = [m for m in self._mock_data["marks"] if m["student_id"] != st_id]
            if len(self._mock_data["students"]) < initial_len:
                return True, 1, ""
            return False, 0, "Student record not found."

        # Upsert Attendance
        if "INSERT INTO ATTENDANCE" in q_upper:
            st_id = int(params[0])
            att_date = str(params[1])
            status = str(params[2])
            remarks = str(params[3]) if params[3] is not None else ""
            found = False
            for a in self._mock_data["attendance"]:
                if a["student_id"] == st_id and str(a["attendance_date"]) == att_date:
                    a["status"] = status
                    a["remarks"] = remarks
                    found = True
                    break
            if not found:
                new_att_id = max([a["id"] for a in self._mock_data["attendance"]] or [0]) + 1
                self._mock_data["attendance"].append({
                    "id": new_att_id,
                    "student_id": st_id,
                    "attendance_date": att_date,
                    "status": status,
                    "remarks": remarks,
                })
            return True, 1, ""

        # Insert Marks
        if "INSERT INTO MARKS" in q_upper:
            new_m_id = max([m["id"] for m in self._mock_data["marks"]] or [0]) + 1
            self._mock_data["marks"].append({
                "id": new_m_id,
                "student_id": int(params[0]),
                "subject": str(params[1]),
                "exam_name": str(params[2]),
                "marks_obtained": float(params[3]),
                "max_marks": float(params[4]),
                "percentage": float(params[5]),
                "grade": str(params[6]),
                "remarks": str(params[7]) if params[7] else "",
            })
            return True, new_m_id, ""

        # Update Marks
        if "UPDATE MARKS" in q_upper:
            m_id = int(params[8])
            for m in self._mock_data["marks"]:
                if m["id"] == m_id:
                    m["student_id"] = int(params[0])
                    m["subject"] = str(params[1])
                    m["exam_name"] = str(params[2])
                    m["marks_obtained"] = float(params[3])
                    m["max_marks"] = float(params[4])
                    m["percentage"] = float(params[5])
                    m["grade"] = str(params[6])
                    m["remarks"] = str(params[7]) if params[7] else ""
                    return True, 1, ""
            return False, 0, "Marks entry not found."

        # Delete Marks
        if "DELETE FROM MARKS" in q_upper:
            m_id = int(params[0])
            self._mock_data["marks"] = [m for m in self._mock_data["marks"] if m["id"] != m_id]
            return True, 1, ""

        # Insert Department
        if "INSERT INTO DEPARTMENTS" in q_upper:
            code = params[0]
            name = params[1]
            for d in self._mock_data["departments"]:
                if d["code"].lower() == code.lower() or d["name"].lower() == name.lower():
                    return False, 0, f"Department code '{code}' or name '{name}' already exists."

            new_d_id = max([d["id"] for d in self._mock_data["departments"]] or [0]) + 1
            self._mock_data["departments"].append({
                "id": new_d_id,
                "code": params[0],
                "name": params[1],
                "description": params[2],
                "status": params[3],
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            })
            return True, new_d_id, ""

        # Update Department
        if "UPDATE DEPARTMENTS" in q_upper:
            d_id = int(params[4])
            for d in self._mock_data["departments"]:
                if d["id"] == d_id:
                    d["code"] = params[0]
                    d["name"] = params[1]
                    d["description"] = params[2]
                    d["status"] = params[3]
                    d["updated_at"] = datetime.now()
                    return True, 1, ""
            return False, 0, "Department not found."

        # Delete Department
        if "DELETE FROM DEPARTMENTS" in q_upper:
            d_id = int(params[0])
            has_students = any(s["department_id"] == d_id for s in self._mock_data["students"])
            if has_students:
                return False, 0, "Cannot delete department because students are assigned to it."
            self._mock_data["departments"] = [d for d in self._mock_data["departments"] if d["id"] != d_id]
            return True, 1, ""

        return True, 1, ""

    def _get_dept_name(self, dept_id: Any) -> str:
        for d in self._mock_data.get("departments", []):
            if d["id"] == dept_id:
                return str(d.get("name", "Unknown"))
        return "Unknown Department"

    def _enrich_students(self, st_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        enriched = []
        for s in st_list:
            item = dict(s)
            dept = next((d for d in self._mock_data.get("departments", []) if d["id"] == s.get("department_id")), None)
            item["department_name"] = dept["name"] if dept else "Unassigned"
            item["department_code"] = dept["code"] if dept else "N/A"
            enriched.append(item)
        return enriched


def get_db() -> DatabaseConnection:
    """Returns singleton DatabaseConnection instance."""
    return DatabaseConnection()
