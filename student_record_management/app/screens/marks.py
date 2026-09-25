"""
Examination marks and grade evaluation screen.
Provides an entry form with automated percentage and letter grade calculation,
along with an audit table of recorded scores.
"""

from typing import Dict, List, Optional
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex

from app.config.settings import Settings
from app.services.student_service import StudentService
from app.services.marks_service import MarksService
from app.utils.constants import COMMON_SUBJECTS, EXAM_TYPES
from app.utils.helpers import calculate_grade
from app.utils.validators import validate_marks
from app.widgets.dialogs import ConfirmDialog, InfoDialog


class MarksScreen(Screen):
    """
    Academic grading and examination score management screen.
    """

    def __init__(self, switch_screen_cb, **kwargs) -> None:
        super().__init__(**kwargs)
        self.switch_screen = switch_screen_cb
        self.student_service = StudentService()
        self.marks_service = MarksService()
        self.student_map: Dict[str, int] = {}
        self.editing_mark_id: Optional[int] = None

        # Root layout
        root = BoxLayout(orientation="vertical", spacing=12, padding=[20, 16, 20, 16])

        # Header Title
        title_box = BoxLayout(orientation="vertical", size_hint_y=None, height=44, spacing=2)
        title_lbl = Label(
            text="Examination Marks & Results",
            font_size="22sp",
            bold=True,
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_y=None,
            height=28,
            halign="left",
            valign="middle",
        )
        title_lbl.bind(size=title_lbl.setter("text_size"))
        title_box.add_widget(title_lbl)

        sub_lbl = Label(
            text="Record subject scores, automatically compute percentages, and assign letter grades",
            font_size="12sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_y=None,
            height=16,
            halign="left",
            valign="middle",
        )
        sub_lbl.bind(size=sub_lbl.setter("text_size"))
        title_box.add_widget(sub_lbl)
        root.add_widget(title_box)

        # Form Card for Entering / Editing Marks
        form_card = BoxLayout(orientation="vertical", size_hint_y=None, height=190, padding=16, spacing=10)
        with form_card.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_SURFACE))
            form_card.bg = RoundedRectangle(pos=form_card.pos, size=form_card.size, radius=[6, 6, 6, 6])
            Color(*get_color_from_hex(Settings.COLOR_BORDER))
            form_card.line = Line(rounded_rectangle=[form_card.x, form_card.y, form_card.width, form_card.height, 6], width=1)

        def _upd_fc(ins, *args):
            ins.bg.pos = ins.pos
            ins.bg.size = ins.size
            ins.line.rounded_rectangle = [ins.x, ins.y, ins.width, ins.height, 6]

        form_card.bind(pos=_upd_fc, size=_upd_fc)

        form_hdr = Label(
            text="Score Entry Form",
            bold=True,
            font_size="14sp",
            color=get_color_from_hex(Settings.COLOR_PRIMARY),
            size_hint_y=None,
            height=20,
            halign="left",
            valign="middle",
        )
        form_hdr.bind(size=form_hdr.setter("text_size"))
        form_card.add_widget(form_hdr)

        # Form Grid Row 1: Student Spinner, Subject Spinner, Exam Spinner
        row1 = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=40)

        # Student Spinner
        self.spn_student = Spinner(
            text="Select Student",
            values=["Select Student"],
            size_hint_x=0.45,
            background_color=get_color_from_hex(Settings.COLOR_BACKGROUND),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        row1.add_widget(self.spn_student)

        # Subject Spinner
        self.spn_subject = Spinner(
            text=COMMON_SUBJECTS[0],
            values=COMMON_SUBJECTS,
            size_hint_x=0.35,
            background_color=get_color_from_hex(Settings.COLOR_BACKGROUND),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        row1.add_widget(self.spn_subject)

        # Exam Name Spinner
        self.spn_exam = Spinner(
            text=EXAM_TYPES[2],  # Sem Exam
            values=EXAM_TYPES,
            size_hint_x=0.20,
            background_color=get_color_from_hex(Settings.COLOR_BACKGROUND),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        row1.add_widget(self.spn_exam)
        form_card.add_widget(row1)

        # Form Grid Row 2: Marks Obtained, Max Marks, Computed Grade Preview, Save Button
        row2 = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=40)

        self.inp_marks = TextInput(
            hint_text="Score (e.g. 85.5)",
            multiline=False,
            size_hint_x=0.22,
            font_size="13sp",
            padding=[8, 8, 8, 8],
            background_color=get_color_from_hex(Settings.COLOR_BACKGROUND),
            foreground_color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        self.inp_marks.bind(text=lambda ins, val: self._update_grade_preview())
        row2.add_widget(self.inp_marks)

        self.inp_max = TextInput(
            text="100.00",
            hint_text="Max Marks",
            multiline=False,
            size_hint_x=0.20,
            font_size="13sp",
            padding=[8, 8, 8, 8],
            background_color=get_color_from_hex(Settings.COLOR_BACKGROUND),
            foreground_color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        self.inp_max.bind(text=lambda ins, val: self._update_grade_preview())
        row2.add_widget(self.inp_max)

        # Grade Preview Pill
        self.lbl_preview = Label(
            text="Grade: — (%)",
            bold=True,
            font_size="13sp",
            color=get_color_from_hex(Settings.COLOR_PRIMARY),
            size_hint_x=0.25,
            halign="center",
            valign="middle",
        )
        row2.add_widget(self.lbl_preview)

        # Save Button
        btn_save = Button(
            text="Record Score",
            bold=True,
            font_size="12sp",
            size_hint_x=0.20,
            background_color=get_color_from_hex(Settings.COLOR_PRIMARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_save.bind(on_release=lambda x: self.save_marks())
        row2.add_widget(btn_save)

        # Reset button
        btn_clear = Button(
            text="Clear",
            font_size="12sp",
            size_hint_x=0.13,
            background_color=get_color_from_hex(Settings.COLOR_BORDER),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        btn_clear.bind(on_release=lambda x: self.reset_form())
        row2.add_widget(btn_clear)

        form_card.add_widget(row2)

        # Form error feedback
        self.lbl_form_error = Label(
            text="",
            font_size="11sp",
            bold=True,
            color=get_color_from_hex(Settings.COLOR_ERROR),
            size_hint_y=None,
            height=16,
            halign="left",
            valign="middle",
        )
        self.lbl_form_error.bind(size=self.lbl_form_error.setter("text_size"))
        form_card.add_widget(self.lbl_form_error)

        root.add_widget(form_card)

        # Table Section Header
        lbl_list_hdr = Label(
            text="Recorded Examination Scores",
            bold=True,
            font_size="15sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_y=None,
            height=26,
            halign="left",
            valign="middle",
        )
        lbl_list_hdr.bind(size=lbl_list_hdr.setter("text_size"))
        root.add_widget(lbl_list_hdr)

        # Table Column Header
        tbl_hdr = BoxLayout(orientation="horizontal", size_hint_y=None, height=32, padding=[12, 4, 12, 4], spacing=10)
        with tbl_hdr.canvas.before:
            Color(*get_color_from_hex("#E2E8F0"))
            tbl_hdr.bg = RoundedRectangle(pos=tbl_hdr.pos, size=tbl_hdr.size, radius=[4, 4, 0, 0])

        def _upd_th2(ins, *args):
            ins.bg.pos = ins.pos
            ins.bg.size = ins.size

        tbl_hdr.bind(pos=_upd_th2, size=_upd_th2)

        tbl_hdr.add_widget(self._th_cell("Student", flex=1))
        tbl_hdr.add_widget(self._th_cell("Subject", flex=1))
        tbl_hdr.add_widget(self._th_cell("Exam", width=120))
        tbl_hdr.add_widget(self._th_cell("Score", width=100))
        tbl_hdr.add_widget(self._th_cell("Grade", width=70))
        tbl_hdr.add_widget(self._th_cell("Action", width=70))
        root.add_widget(tbl_hdr)

        # Scrollable Marks List
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.rows_box = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None)
        self.rows_box.bind(minimum_height=self.rows_box.setter("height"))

        scroll.add_widget(self.rows_box)
        root.add_widget(scroll)
        self.add_widget(root)

    def _th_cell(self, text: str, width: Optional[int] = None, flex: Optional[int] = None) -> Label:
        l = Label(
            text=text,
            bold=True,
            font_size="11sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            halign="left",
            valign="middle",
        )
        l.bind(size=l.setter("text_size"))
        if width:
            l.size_hint_x = None
            l.width = width
        elif flex:
            l.size_hint_x = flex
        return l

    def on_enter(self) -> None:
        """Loads students dropdown and records list."""
        self.load_students()
        self.load_marks_list()

    def load_students(self) -> None:
        """Populates the student selection spinner."""
        students = self.student_service.get_all()
        self.student_map = {}
        names = []
        for s in students:
            label = f"{s.admission_number} - {s.full_name}"
            self.student_map[label] = s.id  # type: ignore
            names.append(label)
        self.spn_student.values = names
        if names and self.spn_student.text == "Select Student":
            self.spn_student.text = names[0]

    def _update_grade_preview(self) -> None:
        """Computes live percentage and grade indicator as user types."""
        val = self.inp_marks.text.strip()
        mx = self.inp_max.text.strip()
        valid, _, ob, m_val = validate_marks(val, mx)
        if valid and m_val > 0:
            pct = round((ob / m_val * 100), 1)
            gr = calculate_grade(pct)
            self.lbl_preview.text = f"Grade: {gr} ({pct}%)"
            self.lbl_preview.color = get_color_from_hex(Settings.COLOR_SUCCESS if pct >= 50 else Settings.COLOR_ERROR)
        else:
            self.lbl_preview.text = "Grade: — (%)"
            self.lbl_preview.color = get_color_from_hex(Settings.COLOR_TEXT_SECONDARY)

    def reset_form(self) -> None:
        """Resets the input fields."""
        self.editing_mark_id = None
        self.inp_marks.text = ""
        self.inp_max.text = "100.00"
        self.lbl_preview.text = "Grade: — (%)"
        self.lbl_form_error.text = ""

    def save_marks(self) -> None:
        """Validates inputs and saves marks entry."""
        st_label = self.spn_student.text
        student_id = self.student_map.get(st_label, 0)
        subject = self.spn_subject.text.strip()
        exam_name = self.spn_exam.text.strip()
        marks_str = self.inp_marks.text.strip()
        max_str = self.inp_max.text.strip()

        if self.editing_mark_id:
            ok, msg = self.marks_service.update_marks(
                self.editing_mark_id, student_id, subject, exam_name, marks_str, max_str
            )
        else:
            ok, msg, _ = self.marks_service.record_marks(
                student_id, subject, exam_name, marks_str, max_str
            )

        if ok:
            self.reset_form()
            self.load_marks_list()
            InfoDialog("Success", msg).open()
        else:
            self.lbl_form_error.text = msg

    def load_marks_list(self) -> None:
        """Fetches all marks records from database."""
        all_marks = self.marks_service.get_all()
        self.rows_box.clear_widgets()

        if not all_marks:
            lbl_empty = Label(
                text="No examination scores recorded yet.",
                font_size="13sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                size_hint_y=None,
                height=50,
            )
            self.rows_box.add_widget(lbl_empty)
            return

        for m in all_marks:
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, padding=[12, 4, 12, 4], spacing=10)
            with row.canvas.before:
                Color(*get_color_from_hex(Settings.COLOR_SURFACE))
                row.bg = RoundedRectangle(pos=row.pos, size=row.size, radius=[4, 4, 4, 4])
                Color(*get_color_from_hex(Settings.COLOR_BORDER))
                row.line = Line(rounded_rectangle=[row.x, row.y, row.width, row.height, 4], width=1)

            def _upd_r2(ins, *args):
                ins.bg.pos = ins.pos
                ins.bg.size = ins.size
                ins.line.rounded_rectangle = [ins.x, ins.y, ins.width, ins.height, 4]

            row.bind(pos=_upd_r2, size=_upd_r2)

            # Student Name
            st_l = Label(
                text=f"{m.admission_number} - {m.student_name}",
                bold=True,
                font_size="11sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
                size_hint_x=1,
                halign="left",
                valign="middle",
            )
            st_l.bind(size=st_l.setter("text_size"))
            row.add_widget(st_l)

            # Subject
            sub_l = Label(
                text=m.subject,
                font_size="11sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                size_hint_x=1,
                halign="left",
                valign="middle",
            )
            sub_l.bind(size=sub_l.setter("text_size"))
            row.add_widget(sub_l)

            # Exam
            exam_l = Label(
                text=m.exam_name,
                font_size="11sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                size_hint_x=None,
                width=120,
                halign="left",
                valign="middle",
            )
            exam_l.bind(size=exam_l.setter("text_size"))
            row.add_widget(exam_l)

            # Score
            score_l = Label(
                text=f"{m.marks_obtained:.1f} / {m.max_marks:.0f}",
                bold=True,
                font_size="11sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
                size_hint_x=None,
                width=100,
                halign="left",
                valign="middle",
            )
            score_l.bind(size=score_l.setter("text_size"))
            row.add_widget(score_l)

            # Grade
            grade_l = Label(
                text=f"{m.grade} ({m.percentage:.1f}%)",
                bold=True,
                font_size="11sp",
                color=get_color_from_hex(Settings.COLOR_PRIMARY),
                size_hint_x=None,
                width=70,
                halign="left",
                valign="middle",
            )
            grade_l.bind(size=grade_l.setter("text_size"))
            row.add_widget(grade_l)

            # Delete Button
            btn_del = Button(
                text="Delete",
                font_size="10sp",
                size_hint=(None, None),
                size=(60, 28),
                background_color=get_color_from_hex(Settings.COLOR_ERROR),
                color=get_color_from_hex("#FFFFFF"),
            )
            btn_del.bind(on_release=lambda x, m_id=m.id: self.delete_marks(m_id))  # type: ignore
            row.add_widget(btn_del)

            self.rows_box.add_widget(row)

    def delete_marks(self, mark_id: int) -> None:
        """Deletes a marks record."""
        def confirm():
            ok, msg = self.marks_service.delete_marks(mark_id)
            if ok:
                self.load_marks_list()
                InfoDialog("Deleted", "Marks entry removed.").open()
            else:
                InfoDialog("Error", msg, is_error=True).open()

        ConfirmDialog(
            title="Delete Marks Entry",
            message="Are you sure you want to delete this examination score?",
            on_confirm=confirm,
        ).open()
