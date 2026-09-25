"""
Comprehensive student profile and academic dossier screen.
Displays personal, contact, academic, guardian, attendance statistics,
and examination results with direct Edit and Delete capabilities.
"""

from typing import Optional
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex

from app.config.settings import Settings
from app.models.student import Student
from app.services.student_service import StudentService
from app.services.attendance_service import AttendanceService
from app.services.marks_service import MarksService
from app.widgets.dialogs import ConfirmDialog, InfoDialog


class StudentDetailsScreen(Screen):
    """
    Dedicated 360-degree Student Profile view.
    """

    def __init__(self, switch_screen_cb, **kwargs) -> None:
        super().__init__(**kwargs)
        self.switch_screen = switch_screen_cb
        self.student_service = StudentService()
        self.attendance_service = AttendanceService()
        self.marks_service = MarksService()
        self.current_student_id: Optional[int] = None
        self.current_student: Optional[Student] = None

        # Main Layout
        root = BoxLayout(orientation="vertical", spacing=12, padding=[20, 16, 20, 16])

        # Header Action Bar
        top_bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=42, spacing=10)

        btn_back = Button(
            text="← Back to Directory",
            font_size="12sp",
            size_hint=(None, None),
            size=(140, 36),
            background_color=get_color_from_hex(Settings.COLOR_BORDER),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        btn_back.bind(on_release=lambda x: self.switch_screen("students"))
        top_bar.add_widget(btn_back)

        self.lbl_profile_title = Label(
            text="Student Profile",
            font_size="20sp",
            bold=True,
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_x=1,
            halign="left",
            valign="middle",
        )
        self.lbl_profile_title.bind(size=self.lbl_profile_title.setter("text_size"))
        top_bar.add_widget(self.lbl_profile_title)

        # Action: Edit Profile
        btn_edit = Button(
            text="Edit Student",
            font_size="12sp",
            bold=True,
            size_hint=(None, None),
            size=(110, 36),
            background_color=get_color_from_hex(Settings.COLOR_SECONDARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_edit.bind(on_release=lambda x: self.handle_edit())
        top_bar.add_widget(btn_edit)

        # Action: Delete Profile
        btn_del = Button(
            text="Delete",
            font_size="12sp",
            bold=True,
            size_hint=(None, None),
            size=(90, 36),
            background_color=get_color_from_hex(Settings.COLOR_ERROR),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_del.bind(on_release=lambda x: self.handle_delete())
        top_bar.add_widget(btn_del)

        root.add_widget(top_bar)

        # Scrollable profile content
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.content_box = BoxLayout(orientation="vertical", spacing=16, size_hint_y=None, padding=[2, 4, 2, 16])
        self.content_box.bind(minimum_height=self.content_box.setter("height"))

        scroll.add_widget(self.content_box)
        root.add_widget(scroll)
        self.add_widget(root)

    def load_student(self, student_id: int) -> None:
        """Fetches full student dossier and builds UI cards."""
        self.current_student_id = student_id
        st = self.student_service.get_by_id(student_id)
        self.current_student = st
        self.content_box.clear_widgets()

        if not st:
            lbl_err = Label(
                text="Student record could not be found.",
                font_size="14sp",
                color=get_color_from_hex(Settings.COLOR_ERROR),
                size_hint_y=None,
                height=60,
            )
            self.content_box.add_widget(lbl_err)
            return

        self.lbl_profile_title.text = f"{st.full_name} ({st.admission_number})"

        # 1. Summary Header Card
        header_card = BoxLayout(orientation="horizontal", size_hint_y=None, height=84, padding=16, spacing=14)
        with header_card.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_PRIMARY_DARK))
            header_card.bg = RoundedRectangle(pos=header_card.pos, size=header_card.size, radius=[6, 6, 6, 6])

        def _update_hdr_bg(instance, *args):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size

        header_card.bind(pos=_update_hdr_bg, size=_update_hdr_bg)

        # Student Name and Admission No in Header
        st_name_box = BoxLayout(orientation="vertical", spacing=4, size_hint_x=1)
        name_l = Label(
            text=st.full_name,
            font_size="18sp",
            bold=True,
            color=get_color_from_hex("#FFFFFF"),
            size_hint_y=None,
            height=26,
            halign="left",
            valign="middle",
        )
        name_l.bind(size=name_l.setter("text_size"))
        st_name_box.add_widget(name_l)

        meta_l = Label(
            text=f"Admission: {st.admission_number} | {st.department_name} | Year {st.year} | Status: {st.status}",
            font_size="12sp",
            color=get_color_from_hex("#CBD5E1"),
            size_hint_y=None,
            height=20,
            halign="left",
            valign="middle",
        )
        meta_l.bind(size=meta_l.setter("text_size"))
        st_name_box.add_widget(meta_l)
        header_card.add_widget(st_name_box)

        # Quick Attendance Stat Pill
        att_stat = self.attendance_service.get_summary_for_student(student_id)
        att_box = BoxLayout(orientation="vertical", size_hint_x=None, width=130, spacing=2)
        att_title = Label(
            text="ATTENDANCE",
            font_size="10sp",
            bold=True,
            color=get_color_from_hex("#94A3B8"),
            size_hint_y=None,
            height=16,
        )
        att_val = Label(
            text=f"{att_stat['percentage']}%",
            font_size="22sp",
            bold=True,
            color=get_color_from_hex(Settings.COLOR_SUCCESS if att_stat['percentage'] >= 75 else Settings.COLOR_WARNING),
            size_hint_y=None,
            height=30,
        )
        att_box.add_widget(att_title)
        att_box.add_widget(att_val)
        header_card.add_widget(att_box)

        self.content_box.add_widget(header_card)

        # 2. Information Section Grid: Personal & Contact (Left) and Academic & Guardian (Right)
        grid_info = GridLayout(cols=2, spacing=14, size_hint_y=None, height=270)

        # Left Card: Personal & Contact Info
        left_card = self._create_info_card("Personal & Contact Details", [
            ("Student ID", str(st.id)),
            ("Gender", st.gender),
            ("Date of Birth", str(st.date_of_birth)),
            ("Email Address", st.email),
            ("Phone Number", st.phone_number),
            ("Residential Address", st.address),
        ])
        grid_info.add_widget(left_card)

        # Right Card: Academic & Guardian Info
        right_card = self._create_info_card("Academic & Guardian Information", [
            ("Department / Major", st.department_name),
            ("Academic Year", f"Year {st.year}"),
            ("Admission Date", str(st.admission_date)),
            ("Account Status", st.status),
            ("Guardian Name", st.guardian_name),
            ("Guardian Phone", st.guardian_phone),
        ])
        grid_info.add_widget(right_card)

        self.content_box.add_widget(grid_info)

        # 3. Academic Marks & Grades Dossier
        marks_section = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None, height=210)
        marks_title = Label(
            text="Academic Evaluation & Marks Transcript",
            bold=True,
            font_size="15sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_y=None,
            height=26,
            halign="left",
            valign="middle",
        )
        marks_title.bind(size=marks_title.setter("text_size"))
        marks_section.add_widget(marks_title)

        student_marks = self.marks_service.get_by_student(student_id)
        if not student_marks:
            lbl_no_marks = Label(
                text="No examination scores recorded yet for this student.",
                font_size="12sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                size_hint_y=None,
                height=40,
                halign="left",
            )
            marks_section.add_widget(lbl_no_marks)
        else:
            marks_list = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None)
            marks_list.bind(minimum_height=marks_list.setter("height"))

            for m in student_marks[:5]:
                m_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=36, padding=[12, 6, 12, 6], spacing=10)
                with m_row.canvas.before:
                    Color(*get_color_from_hex(Settings.COLOR_SURFACE))
                    m_row.bg = RoundedRectangle(pos=m_row.pos, size=m_row.size, radius=[4, 4, 4, 4])
                    Color(*get_color_from_hex(Settings.COLOR_BORDER))
                    m_row.line = Line(rounded_rectangle=[m_row.x, m_row.y, m_row.width, m_row.height, 4], width=1)

                def _upd_m(ins, *args):
                    ins.bg.pos = ins.pos
                    ins.bg.size = ins.size
                    ins.line.rounded_rectangle = [ins.x, ins.y, ins.width, ins.height, 4]

                m_row.bind(pos=_upd_m, size=_upd_m)

                lbl_sub = Label(
                    text=f"{m.subject} ({m.exam_name})",
                    font_size="12sp",
                    bold=True,
                    color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
                    size_hint_x=1,
                    halign="left",
                    valign="middle",
                )
                lbl_sub.bind(size=lbl_sub.setter("text_size"))
                m_row.add_widget(lbl_sub)

                lbl_score = Label(
                    text=f"{m.marks_obtained:.1f} / {m.max_marks:.1f} ({m.percentage:.1f}%)",
                    font_size="12sp",
                    color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                    size_hint_x=None,
                    width=150,
                    halign="right",
                    valign="middle",
                )
                lbl_score.bind(size=lbl_score.setter("text_size"))
                m_row.add_widget(lbl_score)

                lbl_grade = Label(
                    text=f"Grade: {m.grade}",
                    bold=True,
                    font_size="12sp",
                    color=get_color_from_hex(Settings.COLOR_PRIMARY),
                    size_hint_x=None,
                    width=75,
                    halign="center",
                    valign="middle",
                )
                m_row.add_widget(lbl_grade)

                marks_list.add_widget(m_row)

            marks_section.add_widget(marks_list)

        self.content_box.add_widget(marks_section)

    def _create_info_card(self, title: str, pairs: list) -> BoxLayout:
        """Builds a structured card with labeled data pairs."""
        card = BoxLayout(orientation="vertical", spacing=8, padding=16, size_hint_y=None, height=270)
        with card.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_SURFACE))
            card.bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[6, 6, 6, 6])
            Color(*get_color_from_hex(Settings.COLOR_BORDER))
            card.line = Line(rounded_rectangle=[card.x, card.y, card.width, card.height, 6], width=1)

        def _update(instance, *args):
            instance.bg.pos = instance.pos
            instance.bg.size = instance.size
            instance.line.rounded_rectangle = [instance.x, instance.y, instance.width, instance.height, 6]

        card.bind(pos=_update, size=_update)

        lbl_head = Label(
            text=title,
            bold=True,
            font_size="13sp",
            color=get_color_from_hex(Settings.COLOR_PRIMARY),
            size_hint_y=None,
            height=20,
            halign="left",
            valign="middle",
        )
        lbl_head.bind(size=lbl_head.setter("text_size"))
        card.add_widget(lbl_head)

        for label, val in pairs:
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=26)
            k_lbl = Label(
                text=label,
                font_size="11sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                size_hint_x=None,
                width=140,
                halign="left",
                valign="middle",
            )
            k_lbl.bind(size=k_lbl.setter("text_size"))
            row.add_widget(k_lbl)

            v_lbl = Label(
                text=str(val or "—"),
                bold=True,
                font_size="11sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
                size_hint_x=1,
                halign="left",
                valign="middle",
            )
            v_lbl.bind(size=v_lbl.setter("text_size"))
            row.add_widget(v_lbl)
            card.add_widget(row)

        return card

    def handle_edit(self) -> None:
        """Transitions to student form with active student ID."""
        if self.current_student_id:
            self.switch_screen("student_form", self.current_student_id)

    def handle_delete(self) -> None:
        """Prompts confirmation dialog and executes student deletion."""
        if not self.current_student:
            return

        def do_delete():
            ok, msg = self.student_service.delete(self.current_student.id)  # type: ignore
            if ok:
                InfoDialog("Record Deleted", f"Student '{self.current_student.full_name}' was removed.", on_close=lambda: self.switch_screen("students")).open()
            else:
                InfoDialog("Error", msg, is_error=True).open()

        ConfirmDialog(
            title="Delete Student",
            message=f"Are you sure you want to permanently delete\n{self.current_student.full_name} ({self.current_student.admission_number})?",
            on_confirm=do_delete,
        ).open()
