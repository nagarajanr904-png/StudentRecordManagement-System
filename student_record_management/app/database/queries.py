"""
Centralized parameterized SQL queries for the Student Record Management System.
All statements use standard parameterized placeholders (%s) to strictly prevent SQL injection.
"""

# ==============================================================================
# Department Queries
# ==============================================================================
SELECT_ALL_DEPARTMENTS = """
    SELECT d.id, d.code, d.name, d.description, d.status, d.created_at, d.updated_at,
           COUNT(s.id) AS student_count
    FROM departments d
    LEFT JOIN students s ON s.department_id = d.id
    GROUP BY d.id, d.code, d.name, d.description, d.status, d.created_at, d.updated_at
    ORDER BY d.name ASC;
"""

SELECT_ACTIVE_DEPARTMENTS = """
    SELECT id, code, name, description, status, created_at, updated_at
    FROM departments
    WHERE status = 'Active'
    ORDER BY name ASC;
"""

SELECT_DEPARTMENT_BY_ID = """
    SELECT id, code, name, description, status, created_at, updated_at
    FROM departments
    WHERE id = %s;
"""

INSERT_DEPARTMENT = """
    INSERT INTO departments (code, name, description, status)
    VALUES (%s, %s, %s, %s);
"""

UPDATE_DEPARTMENT = """
    UPDATE departments
    SET code = %s, name = %s, description = %s, status = %s
    WHERE id = %s;
"""

DELETE_DEPARTMENT = """
    DELETE FROM departments
    WHERE id = %s;
"""

CHECK_DEPARTMENT_STUDENTS = """
    SELECT COUNT(*) AS count
    FROM students
    WHERE department_id = %s;
"""


# ==============================================================================
# Student Queries
# ==============================================================================
SELECT_ALL_STUDENTS = """
    SELECT s.id, s.admission_number, s.first_name, s.last_name, s.gender,
           s.date_of_birth, s.phone_number, s.email, s.address, s.department_id,
           s.year, s.guardian_name, s.guardian_phone, s.admission_date, s.status,
           s.created_date, s.updated_date,
           d.name AS department_name, d.code AS department_code
    FROM students s
    LEFT JOIN departments d ON s.department_id = d.id
    ORDER BY s.id DESC;
"""

SELECT_STUDENT_BY_ID = """
    SELECT s.id, s.admission_number, s.first_name, s.last_name, s.gender,
           s.date_of_birth, s.phone_number, s.email, s.address, s.department_id,
           s.year, s.guardian_name, s.guardian_phone, s.admission_date, s.status,
           s.created_date, s.updated_date,
           d.name AS department_name, d.code AS department_code
    FROM students s
    LEFT JOIN departments d ON s.department_id = d.id
    WHERE s.id = %s;
"""

SELECT_STUDENT_BY_ADMISSION_NUMBER = """
    SELECT id, admission_number, first_name, last_name, email
    FROM students
    WHERE admission_number = %s;
"""

SEARCH_STUDENTS = """
    SELECT s.id, s.admission_number, s.first_name, s.last_name, s.gender,
           s.date_of_birth, s.phone_number, s.email, s.address, s.department_id,
           s.year, s.guardian_name, s.guardian_phone, s.admission_date, s.status,
           s.created_date, s.updated_date,
           d.name AS department_name, d.code AS department_code
    FROM students s
    LEFT JOIN departments d ON s.department_id = d.id
    WHERE (
        LOWER(s.admission_number) LIKE LOWER(%s)
        OR LOWER(s.first_name) LIKE LOWER(%s)
        OR LOWER(s.last_name) LIKE LOWER(%s)
        OR LOWER(CONCAT(s.first_name, ' ', s.last_name)) LIKE LOWER(%s)
        OR LOWER(s.phone_number) LIKE LOWER(%s)
        OR LOWER(d.name) LIKE LOWER(%s)
        OR CAST(s.id AS CHAR) = %s
    )
    ORDER BY s.id DESC;
"""

INSERT_STUDENT = """
    INSERT INTO students (
        admission_number, first_name, last_name, gender, date_of_birth,
        phone_number, email, address, department_id, year,
        guardian_name, guardian_phone, admission_date, status
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

UPDATE_STUDENT = """
    UPDATE students
    SET admission_number = %s, first_name = %s, last_name = %s, gender = %s,
        date_of_birth = %s, phone_number = %s, email = %s, address = %s,
        department_id = %s, year = %s, guardian_name = %s, guardian_phone = %s,
        admission_date = %s, status = %s
    WHERE id = %s;
"""

UPDATE_STUDENT_STATUS = """
    UPDATE students
    SET status = %s
    WHERE id = %s;
"""

DELETE_STUDENT = """
    DELETE FROM students
    WHERE id = %s;
"""


# ==============================================================================
# Attendance Queries
# ==============================================================================
SELECT_ATTENDANCE_BY_DATE = """
    SELECT a.id, a.student_id, a.attendance_date, a.status, a.remarks,
           a.created_at, a.updated_at,
           s.admission_number, s.first_name, s.last_name, s.year,
           d.name AS department_name
    FROM attendance a
    JOIN students s ON a.student_id = s.id
    LEFT JOIN departments d ON s.department_id = d.id
    WHERE a.attendance_date = %s
    ORDER BY s.last_name ASC, s.first_name ASC;
"""

SELECT_ATTENDANCE_BY_STUDENT = """
    SELECT id, student_id, attendance_date, status, remarks, created_at, updated_at
    FROM attendance
    WHERE student_id = %s
    ORDER BY attendance_date DESC;
"""

SELECT_STUDENT_ATTENDANCE_SUMMARY = """
    SELECT
        COUNT(*) AS total_recorded,
        SUM(CASE WHEN status = 'Present' THEN 1 ELSE 0 END) AS present_count,
        SUM(CASE WHEN status = 'Absent' THEN 1 ELSE 0 END) AS absent_count,
        SUM(CASE WHEN status = 'Late' THEN 1 ELSE 0 END) AS late_count
    FROM attendance
    WHERE student_id = %s;
"""

UPSERT_ATTENDANCE = """
    INSERT INTO attendance (student_id, attendance_date, status, remarks)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE status = VALUES(status), remarks = VALUES(remarks);
"""

DELETE_ATTENDANCE = """
    DELETE FROM attendance
    WHERE id = %s;
"""


# ==============================================================================
# Marks / Results Queries
# ==============================================================================
SELECT_MARKS_BY_STUDENT = """
    SELECT id, student_id, subject, exam_name, marks_obtained, max_marks,
           percentage, grade, remarks, created_at, updated_at
    FROM marks
    WHERE student_id = %s
    ORDER BY exam_name ASC, subject ASC;
"""

SELECT_ALL_MARKS = """
    SELECT m.id, m.student_id, m.subject, m.exam_name, m.marks_obtained,
           m.max_marks, m.percentage, m.grade, m.remarks, m.created_at,
           s.admission_number, s.first_name, s.last_name, d.name AS department_name
    FROM marks m
    JOIN students s ON m.student_id = s.id
    LEFT JOIN departments d ON s.department_id = d.id
    ORDER BY m.id DESC;
"""

INSERT_MARKS = """
    INSERT INTO marks (
        student_id, subject, exam_name, marks_obtained, max_marks,
        percentage, grade, remarks
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
"""

UPDATE_MARKS = """
    UPDATE marks
    SET student_id = %s, subject = %s, exam_name = %s, marks_obtained = %s,
        max_marks = %s, percentage = %s, grade = %s, remarks = %s
    WHERE id = %s;
"""

DELETE_MARKS = """
    DELETE FROM marks
    WHERE id = %s;
"""


# ==============================================================================
# Dashboard / Statistics Queries
# ==============================================================================
DASHBOARD_METRICS = """
    SELECT
        (SELECT COUNT(*) FROM students) AS total_students,
        (SELECT COUNT(*) FROM students WHERE status = 'Active') AS active_students,
        (SELECT COUNT(*) FROM students WHERE gender = 'Male') AS male_students,
        (SELECT COUNT(*) FROM students WHERE gender = 'Female') AS female_students,
        (SELECT COUNT(*) FROM departments WHERE status = 'Active') AS total_departments;
"""

RECENT_STUDENTS = """
    SELECT s.id, s.admission_number, s.first_name, s.last_name, s.gender,
           s.year, s.status, s.admission_date, d.name AS department_name
    FROM students s
    LEFT JOIN departments d ON s.department_id = d.id
    ORDER BY s.id DESC
    LIMIT 5;
"""
