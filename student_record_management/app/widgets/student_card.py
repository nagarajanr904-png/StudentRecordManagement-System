"""
Student record card item used in student directories and search lists.
"""

from typing import Callable, Optional
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex

from app.models.student import Student
from app.config.settings import Settings


class StudentListItem(BoxLayout):
    """
    Individual student card component.
    Displays admission number, name, department, year, status badge,
    and action buttons (View, Edit, Delete).
    """

    def __init__(
        self,
        student: Student,
        on_view: Optional[Callable[[Student], None]] = None,
        on_edit: Optional[Callable[[Student], None]] = None,
        on_delete: Optional[Callable[[Student], None]] = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.student = student
        self.on_view_callback = on_view
        self.on_edit_callback = on_edit
        self.on_delete_callback = on_delete

        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = 110
        self.padding = [16, 12, 16, 12]
        self.spacing = 6

        # Clean background and subtle outline
        with self.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_SURFACE))
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[6, 6, 6, 6])
            Color(*get_color_from_hex(Settings.COLOR_BORDER))
            self.border_line = Line(rounded_rectangle=[self.x, self.y, self.width, self.height, 6], width=1)

        self.bind(pos=self._update_rects, size=self._update_rects)

        # Top row: Name, Admission Number, Status Badge
        top_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=26, spacing=10)

        # Admission number pill
        adm_lbl = Label(
            text=student.admission_number,
            bold=True,
            font_size="12sp",
            color=get_color_from_hex(Settings.COLOR_PRIMARY),
            size_hint_x=None,
            width=110,
            halign="left",
            valign="middle",
        )
        adm_lbl.bind(size=adm_lbl.setter("text_size"))
        top_row.add_widget(adm_lbl)

        # Full name
        name_lbl = Label(
            text=student.full_name,
            bold=True,
            font_size="15sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_x=1,
            halign="left",
            valign="middle",
        )
        name_lbl.bind(size=name_lbl.setter("text_size"))
        top_row.add_widget(name_lbl)

        # Status text
        status_color = Settings.COLOR_SUCCESS if student.status == "Active" else Settings.COLOR_ERROR
        status_lbl = Label(
            text=f"● {student.status}",
            font_size="12sp",
            bold=True,
            color=get_color_from_hex(status_color),
            size_hint_x=None,
            width=80,
            halign="right",
            valign="middle",
        )
        status_lbl.bind(size=status_lbl.setter("text_size"))
        top_row.add_widget(status_lbl)

        self.add_widget(top_row)

        # Middle row: Department, Year, and Contact info
        mid_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=22, spacing=15)
        dept_info = f"{student.department_name} | Year {student.year} | {student.email} | {student.phone_number}"
        details_lbl = Label(
            text=dept_info,
            font_size="12sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_x=1,
            halign="left",
            valign="middle",
        )
        details_lbl.bind(size=details_lbl.setter("text_size"))
        mid_row.add_widget(details_lbl)
        self.add_widget(mid_row)

        # Bottom row: Action Buttons
        btn_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=28, spacing=8)
        btn_row.add_widget(Label(size_hint_x=1))  # Spacer to right align buttons

        # View Profile Button
        btn_view = Button(
            text="View Profile",
            font_size="11sp",
            size_hint_x=None,
            width=90,
            background_color=get_color_from_hex(Settings.COLOR_PRIMARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_view.bind(on_release=lambda x: self.on_view_callback(self.student) if self.on_view_callback else None)
        btn_row.add_widget(btn_view)

        # Edit Button
        btn_edit = Button(
            text="Edit",
            font_size="11sp",
            size_hint_x=None,
            width=65,
            background_color=get_color_from_hex(Settings.COLOR_SECONDARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_edit.bind(on_release=lambda x: self.on_edit_callback(self.student) if self.on_edit_callback else None)
        btn_row.add_widget(btn_edit)

        # Delete Button
        btn_delete = Button(
            text="Delete",
            font_size="11sp",
            size_hint_x=None,
            width=65,
            background_color=get_color_from_hex(Settings.COLOR_ERROR),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_delete.bind(on_release=lambda x: self.on_delete_callback(self.student) if self.on_delete_callback else None)
        btn_row.add_widget(btn_delete)

        self.add_widget(btn_row)

    def _update_rects(self, *args) -> None:
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = [self.x, self.y, self.width, self.height, 6]
