"""
Report generation service.
Produces formatted PDF documents using ReportLab and CSV spreadsheets for
Student Directories, Attendance Records, and Academic Transcripts.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional, Tuple

from app.database.connection import get_db
from app.services.student_service import StudentService
from app.services.attendance_service import AttendanceService
from app.services.marks_service import MarksService
from app.utils.helpers import export_to_csv
from app.config.settings import Settings, logger

# ReportLab imports with graceful error handling
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class NumberedCanvas(canvas.Canvas):  # type: ignore
    """Canvas that computes total pages for professional 'Page X of Y' footers."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states: List[Any] = []

    def showPage(self) -> None:
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self) -> None:
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count: int) -> None:
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748B"))
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 0.75 * inch, 0.5 * inch, page_str)
        self.drawString(0.75 * inch, 0.5 * inch, f"{Settings.APP_NAME} — Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        self.restoreState()


class ReportService:
    """Service handling PDF and CSV report compilation."""

    def __init__(self) -> None:
        self.db = get_db()
        self.student_service = StudentService()
        self.attendance_service = AttendanceService()
        self.marks_service = MarksService()

    def generate_students_pdf(self, output_path: str, department_id: Optional[int] = None) -> Tuple[bool, str]:
        """Generates a clean institutional Student Directory PDF."""
        if not REPORTLAB_AVAILABLE:
            return False, "ReportLab library is not installed. Please run: pip install reportlab"

        students = self.student_service.search(department_id=department_id)
        if not students:
            return False, "No student records found to generate report."

        try:
            doc = SimpleDocTemplate(
                output_path,
                pagesize=landscape(letter),
                leftMargin=36,
                rightMargin=36,
                topMargin=40,
                bottomMargin=50,
            )

            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                "DocTitle",
                parent=styles["Heading1"],
                fontSize=18,
                leading=22,
                textColor=colors.HexColor(Settings.COLOR_PRIMARY),
                spaceAfter=4,
            )
            subtitle_style = ParagraphStyle(
                "DocSubTitle",
                parent=styles["Normal"],
                fontSize=10,
                leading=14,
                textColor=colors.HexColor(Settings.COLOR_TEXT_SECONDARY),
                spaceAfter=15,
            )
            cell_style = ParagraphStyle(
                "TableCell",
                parent=styles["Normal"],
                fontSize=8.5,
                leading=11,
                textColor=colors.HexColor(Settings.COLOR_TEXT_PRIMARY),
            )
            cell_bold = ParagraphStyle(
                "TableCellBold",
                parent=cell_style,
                fontName="Helvetica-Bold",
            )
            header_cell = ParagraphStyle(
                "HeaderCell",
                parent=cell_style,
                fontName="Helvetica-Bold",
                textColor=colors.white,
            )

            story: List[Any] = []
            story.append(Paragraph(f"{Settings.APP_NAME} — Official Student Directory", title_style))
            filter_desc = "All Academic Departments" if not department_id else f"Department ID: {department_id}"
            story.append(
                Paragraph(
                    f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')} | Scope: {filter_desc} | Total Records: {len(students)}",
                    subtitle_style,
                )
            )

            # Table Header
            table_data = [
                [
                    Paragraph("Adm No.", header_cell),
                    Paragraph("Student Name", header_cell),
                    Paragraph("Gender", header_cell),
                    Paragraph("Department", header_cell),
                    Paragraph("Year", header_cell),
                    Paragraph("Phone", header_cell),
                    Paragraph("Email", header_cell),
                    Paragraph("Status", header_cell),
                ]
            ]

            for s in students:
                table_data.append([
                    Paragraph(s.admission_number, cell_bold),
                    Paragraph(s.full_name, cell_style),
                    Paragraph(s.gender, cell_style),
                    Paragraph(s.department_name, cell_style),
                    Paragraph(f"Year {s.year}", cell_style),
                    Paragraph(s.phone_number, cell_style),
                    Paragraph(s.email, cell_style),
                    Paragraph(s.status, cell_style),
                ])

            col_widths = [85, 120, 50, 150, 45, 90, 130, 55]
            t = Table(table_data, colWidths=col_widths, repeatRows=1)
            t.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(Settings.COLOR_PRIMARY)),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor(Settings.COLOR_BORDER)),
            ]))

            story.append(t)
            doc.build(story)
            logger.info("Generated Student Directory PDF at %s", output_path)
            return True, f"Report successfully generated at:\n{output_path}"

        except Exception as e:
            logger.error("Failed to generate PDF: %s", str(e))
            return False, f"Error building PDF document: {str(e)}"

    def generate_students_csv(self, output_path: str, department_id: Optional[int] = None) -> Tuple[bool, str]:
        """Exports students dataset to a CSV file."""
        students = self.student_service.search(department_id=department_id)
        if not students:
            return False, "No student records available for CSV export."

        headers = [
            "ID",
            "Admission Number",
            "First Name",
            "Last Name",
            "Gender",
            "Date of Birth",
            "Department",
            "Year",
            "Email",
            "Phone Number",
            "Address",
            "Guardian Name",
            "Guardian Phone",
            "Admission Date",
            "Status",
        ]

        rows = []
        for s in students:
            rows.append([
                s.id,
                s.admission_number,
                s.first_name,
                s.last_name,
                s.gender,
                s.date_of_birth,
                s.department_name,
                s.year,
                s.email,
                s.phone_number,
                s.address,
                s.guardian_name,
                s.guardian_phone,
                s.admission_date,
                s.status,
            ])

        success = export_to_csv(output_path, headers, rows)
        if success:
            return True, f"CSV exported successfully to:\n{output_path}"
        return False, "Failed to write CSV file. Please check file permissions."

    def generate_attendance_csv(self, output_path: str, target_date: str) -> Tuple[bool, str]:
        """Exports daily attendance list to CSV."""
        records = self.attendance_service.get_by_date(target_date)
        if not records:
            return False, f"No attendance records found for date {target_date}."

        headers = ["Date", "Admission No", "Student Name", "Department", "Year", "Status", "Remarks"]
        rows = [
            [
                r.attendance_date,
                r.admission_number,
                r.student_name,
                r.department_name,
                r.year,
                r.status,
                r.remarks or "",
            ]
            for r in records
        ]

        success = export_to_csv(output_path, headers, rows)
        if success:
            return True, f"Attendance CSV exported to:\n{output_path}"
        return False, "Failed to write attendance CSV file."

    def generate_marks_csv(self, output_path: str) -> Tuple[bool, str]:
        """Exports all marks and academic grades to CSV."""
        records = self.marks_service.get_all()
        if not records:
            return False, "No marks records found to export."

        headers = [
            "Admission No",
            "Student Name",
            "Department",
            "Subject",
            "Exam Name",
            "Marks Obtained",
            "Maximum Marks",
            "Percentage",
            "Grade",
            "Remarks",
        ]
        rows = [
            [
                r.admission_number,
                r.student_name,
                r.department_name,
                r.subject,
                r.exam_name,
                r.marks_obtained,
                r.max_marks,
                f"{r.percentage}%",
                r.grade,
                r.remarks or "",
            ]
            for r in records
        ]

        success = export_to_csv(output_path, headers, rows)
        if success:
            return True, f"Marks CSV exported to:\n{output_path}"
        return False, "Failed to write marks CSV file."
