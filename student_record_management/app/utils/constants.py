"""
Application constants, enumerations, and default options.
"""

GENDERS = ("Male", "Female", "Other")

STUDENT_STATUSES = ("Active", "Inactive", "Suspended", "Graduated")

DEPARTMENT_STATUSES = ("Active", "Inactive")

ATTENDANCE_STATUSES = ("Present", "Absent", "Late")

ACADEMIC_YEARS = (1, 2, 3, 4)

GRADE_SCALE = [
    (90.0, "A+"),
    (80.0, "A"),
    (70.0, "B"),
    (60.0, "C"),
    (50.0, "D"),
    (0.0, "F"),
]

EXAM_TYPES = [
    "Quiz 1",
    "Quiz 2",
    "Sem Exam",
    "Final Exam",
    "Lab Practical",
    "Final Project",
    "Assignment",
]

COMMON_SUBJECTS = [
    "Data Structures & Algorithms",
    "Database Systems",
    "Operating Systems",
    "Computer Networks",
    "Calculus I",
    "Linear Algebra",
    "Digital Signal Processing",
    "Electromagnetic Fields",
    "Thermodynamics",
    "Fluid Mechanics",
    "Robotics & Automation",
    "Principles of Management",
    "Financial Accounting",
    "Marketing Strategy",
    "Microcontrollers",
    "Cloud Architecture",
]

REPORT_TYPES = [
    ("students_full", "Complete Student Directory (PDF)"),
    ("students_csv", "Students List (CSV Spreadsheet)"),
    ("attendance_summary", "Attendance Audit Report (PDF)"),
    ("attendance_csv", "Attendance Records (CSV)"),
    ("marks_summary", "Grade Book & Examination Summary (PDF)"),
    ("marks_csv", "Marks & Results (CSV)"),
]
