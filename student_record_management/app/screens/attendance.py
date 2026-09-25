"""
Student attendance management screen.
Supports daily roll call, Present/Absent/Late toggling, remarks entry,
and date-based attendance auditing.
"""

from datetime import date
from typing import Dict, List, Optional
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex

from app.config.settings import Settings
from app.models.student import Student
from app.services.student_service import StudentService
from app.services.attendance_service import AttendanceService
from app.widgets.dialogs import InfoDialog


class AttendanceScreen(Screen):
    """
    Daily attendance recording and audit interface.
    """

    def __init__(self, switch_screen_cb, **kwargs) -> None:
        super().__init__(**kwargs)
        self.switch_screen = switch_screen_cb
        self.student_service = StudentService()
        self.attendance_service = AttendanceService()
        self.status_toggles: Dict[int, Dict[str, Button]] = {}
        self.remarks_inputs: Dict[int, TextInput] = {}
        self.student_records: List[Student] = []

        # Root layout
        root = BoxLayout(orientation="vertical", spacing=12, padding=[20, 16, 20, 16])

        # Header Title
        title_box = BoxLayout(orientation="vertical", size_hint_y=None, height=44, spacing=2)
        title_lbl = Label(
            text="Attendance Management",
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
            text="Record student presence, absence, and tardiness for daily auditing",
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

        # Date & Filter Bar
        ctrl_bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)

        lbl_date = Label(
            text="Attendance Date:",
            bold=True,
            font_size="12sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_x=None,
            width=110,
            halign="left",
            valign="middle",
        )
        lbl_date.bind(size=lbl_date.setter("text_size"))
        ctrl_bar.add_widget(lbl_date)

        self.inp_date = TextInput(
            text=str(date.today()),
            multiline=False,
            size_hint=(None, None),
            size=(130, 38),
            font_size="13sp",
            padding=[8, 8, 8, 8],
            background_color=get_color_from_hex(Settings.COLOR_SURFACE),
            foreground_color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        self.inp_date.bind(on_text_validate=lambda x: self.load_attendance())
        ctrl_bar.add_widget(self.inp_date)

        btn_load = Button(
            text="Load Records",
            bold=True,
            font_size="12sp",
            size_hint=(None, None),
            size=(110, 38),
            background_color=get_color_from_hex(Settings.COLOR_PRIMARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_load.bind(on_release=lambda x: self.load_attendance())
        ctrl_bar.add_widget(btn_load)

        btn_mark_all = Button(
            text="Mark All Present",
            font_size="12sp",
            size_hint=(None, None),
            size=(130, 38),
            background_color=get_color_from_hex(Settings.COLOR_SUCCESS),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_mark_all.bind(on_release=lambda x: self.mark_all_present())
        ctrl_bar.add_widget(btn_mark_all)

        ctrl_bar.add_widget(Label(size_hint_x=1))  # Spacer

        # Save Attendance Button
        btn_save_all = Button(
            text="Save All Attendance",
            bold=True,
            font_size="12sp",
            size_hint=(None, None),
            size=(160, 38),
            background_color=get_color_from_hex(Settings.COLOR_PRIMARY_DARK),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_save_all.bind(on_release=lambda x: self.save_all_attendance())
        ctrl_bar.add_widget(btn_save_all)

        root.add_widget(ctrl_bar)

        # Table Column Headers
        table_hdr = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=34,
            padding=[12, 6, 12, 6],
            spacing=10,
        )
        with table_hdr.canvas.before:
            Color(*get_color_from_hex("#E2E8F0"))
            table_hdr.bg = RoundedRectangle(pos=table_hdr.pos, size=table_hdr.size, radius=[4, 4, 0, 0])

        def _upd_th(ins, *args):
            ins.bg.pos = ins.pos
            ins.bg.size = ins.size

        table_hdr.bind(pos=_upd_th, size=_upd_th)

        table_hdr.add_widget(self._hdr_label("Adm No.", width=100))
        table_hdr.add_widget(self._hdr_label("Student Name", flex=1))
        table_hdr.add_widget(self._hdr_label("Department", width=180))
        table_hdr.add_widget(self._hdr_label("Attendance Status", width=220))
        table_hdr.add_widget(self._hdr_label("Remarks / Note", width=160))
        root.add_widget(table_hdr)

        # Scrollable rows list
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.rows_container = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None)
        self.rows_container.bind(minimum_height=self.rows_container.setter("height"))

        scroll.add_widget(self.rows_container)
        root.add_widget(scroll)
        self.add_widget(root)

    def _hdr_label(self, text: str, width: Optional[int] = None, flex: Optional[int] = None) -> Label:
        lbl = Label(
            text=text,
            bold=True,
            font_size="11sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            halign="left",
            valign="middle",
        )
        lbl.bind(size=lbl.setter("text_size"))
        if width:
            lbl.size_hint_x = None
            lbl.width = width
        elif flex:
            lbl.size_hint_x = flex
        return lbl

    def on_enter(self) -> None:
        """Loads records when user views screen."""
        self.load_attendance()

    def load_attendance(self) -> None:
        """Fetches active students and existing records for target date."""
        target_date = self.inp_date.text.strip()
        self.student_records = self.student_service.search(status="Active")
        existing_records = self.attendance_service.get_by_date(target_date)
        status_map = {r.student_id: (r.status, r.remarks) for r in existing_records}

        self.rows_container.clear_widgets()
        self.status_toggles.clear()
        self.remarks_inputs.clear()

        if not self.student_records:
            lbl_empty = Label(
                text="No active students found to take attendance.",
                font_size="13sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                size_hint_y=None,
                height=50,
            )
            self.rows_container.add_widget(lbl_empty)
            return

        for st in self.student_records:
            current_status, current_remarks = status_map.get(st.id, ("Present", ""))  # type: ignore

            row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=44,
                padding=[12, 6, 12, 6],
                spacing=10,
            )
            with row.canvas.before:
                Color(*get_color_from_hex(Settings.COLOR_SURFACE))
                row.bg = RoundedRectangle(pos=row.pos, size=row.size, radius=[4, 4, 4, 4])
                Color(*get_color_from_hex(Settings.COLOR_BORDER))
                row.line = Line(rounded_rectangle=[row.x, row.y, row.width, row.height, 4], width=1)

            def _upd_r(ins, *args):
                ins.bg.pos = ins.pos
                ins.bg.size = ins.size
                ins.line.rounded_rectangle = [ins.x, ins.y, ins.width, ins.height, 4]

            row.bind(pos=_upd_r, size=_upd_r)

            # Adm No
            adm_l = Label(
                text=st.admission_number,
                bold=True,
                font_size="11sp",
                color=get_color_from_hex(Settings.COLOR_PRIMARY),
                size_hint_x=None,
                width=100,
                halign="left",
                valign="middle",
            )
            adm_l.bind(size=adm_l.setter("text_size"))
            row.add_widget(adm_l)

            # Name
            name_l = Label(
                text=st.full_name,
                bold=True,
                font_size="12sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
                size_hint_x=1,
                halign="left",
                valign="middle",
            )
            name_l.bind(size=name_l.setter("text_size"))
            row.add_widget(name_l)

            # Dept
            dept_l = Label(
                text=st.department_name,
                font_size="11sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                size_hint_x=None,
                width=180,
                halign="left",
                valign="middle",
            )
            dept_l.bind(size=dept_l.setter("text_size"))
            row.add_widget(dept_l)

            # Status Buttons (Present, Absent, Late)
            btn_box = BoxLayout(orientation="horizontal", size_hint_x=None, width=220, spacing=4)
            toggles = {}
            for stat, color_hex in [("Present", Settings.COLOR_SUCCESS), ("Absent", Settings.COLOR_ERROR), ("Late", Settings.COLOR_WARNING)]:
                btn = Button(
                    text=stat,
                    font_size="10sp",
                    size_hint_x=1,
                    bold=True,
                )
                btn.bind(on_release=lambda x, sid=st.id, s=stat: self._select_status(sid, s))
                toggles[stat] = btn
                btn_box.add_widget(btn)

            self.status_toggles[st.id] = toggles  # type: ignore
            row.add_widget(btn_box)

            # Remarks input
            rem_inp = TextInput(
                text=current_remarks or "",
                hint_text="Optional remarks",
                multiline=False,
                size_hint_x=None,
                width=160,
                font_size="11sp",
                padding=[6, 6, 6, 6],
                background_color=get_color_from_hex(Settings.COLOR_BACKGROUND),
                foreground_color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            )
            self.remarks_inputs[st.id] = rem_inp  # type: ignore
            row.add_widget(rem_inp)

            self._set_button_styles(st.id, current_status)  # type: ignore
            self.rows_container.add_widget(row)

    def _select_status(self, student_id: int, status: str) -> None:
        self._set_button_styles(student_id, status)

    def _set_button_styles(self, student_id: int, active_status: str) -> None:
        toggles = self.status_toggles.get(student_id, {})
        colors = {
            "Present": Settings.COLOR_SUCCESS,
            "Absent": Settings.COLOR_ERROR,
            "Late": Settings.COLOR_WARNING,
        }
        for stat, btn in toggles.items():
            if stat == active_status:
                btn.background_color = get_color_from_hex(colors[stat])
                btn.color = get_color_from_hex("#FFFFFF")
                btn.state = "down"
            else:
                btn.background_color = get_color_from_hex(Settings.COLOR_BORDER)
                btn.color = get_color_from_hex(Settings.COLOR_TEXT_SECONDARY)
                btn.state = "normal"

    def mark_all_present(self) -> None:
        """Sets all toggles to Present."""
        for st in self.student_records:
            self._set_button_styles(st.id, "Present")  # type: ignore

    def save_all_attendance(self) -> None:
        """Iterates through all students and persists attendance entries."""
        target_date = self.inp_date.text.strip()
        saved = 0

        for st in self.student_records:
            sid = st.id
            toggles = self.status_toggles.get(sid, {})  # type: ignore
            active_stat = "Present"
            for stat, btn in toggles.items():
                if btn.state == "down":
                    active_stat = stat
                    break

            remarks = self.remarks_inputs.get(sid, TextInput()).text.strip()  # type: ignore
            ok, _ = self.attendance_service.mark_attendance(sid, target_date, active_stat, remarks)  # type: ignore
            if ok:
                saved += 1

        InfoDialog(
            "Attendance Saved",
            f"Successfully recorded attendance for {saved} students on {target_date}.",
        ).open()
