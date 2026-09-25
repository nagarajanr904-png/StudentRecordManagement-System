"""
Students directory screen.
Provides multi-criteria search, department filters, status toggling,
and actions to view, edit, or delete records.
"""

from typing import List, Optional
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex

from app.config.settings import Settings
from app.models.student import Student
from app.services.student_service import StudentService
from app.services.department_service import DepartmentService
from app.widgets.student_card import StudentListItem
from app.widgets.dialogs import ConfirmDialog, InfoDialog


class StudentsScreen(Screen):
    """
    Main student registry view.
    """

    def __init__(self, switch_screen_cb, **kwargs) -> None:
        super().__init__(**kwargs)
        self.switch_screen = switch_screen_cb
        self.student_service = StudentService()
        self.department_service = DepartmentService()
        self.department_map = {}

        # Root vertical layout
        root = BoxLayout(orientation="vertical", spacing=12, padding=[20, 16, 20, 16])

        # Header Title and Add Button
        head_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=44, spacing=10)
        title_lbl = Label(
            text="Student Directory",
            font_size="22sp",
            bold=True,
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_x=1,
            halign="left",
            valign="middle",
        )
        title_lbl.bind(size=title_lbl.setter("text_size"))
        head_box.add_widget(title_lbl)

        btn_add = Button(
            text="+ Add New Student",
            bold=True,
            font_size="12sp",
            size_hint=(None, None),
            size=(160, 38),
            background_color=get_color_from_hex(Settings.COLOR_PRIMARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_add.bind(on_release=lambda x: self.switch_screen("student_form", None))
        head_box.add_widget(btn_add)
        root.add_widget(head_box)

        # Search & Filter Bar
        filter_bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=42, spacing=8)

        # Search input
        self.txt_search = TextInput(
            hint_text="Search by Name, Admission #, Phone, ID...",
            multiline=False,
            size_hint_x=1,
            font_size="13sp",
            padding=[10, 10, 10, 10],
            background_color=get_color_from_hex(Settings.COLOR_SURFACE),
            foreground_color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        self.txt_search.bind(on_text_validate=lambda x: self.perform_search())
        filter_bar.add_widget(self.txt_search)

        # Department Spinner
        self.spn_dept = Spinner(
            text="All Departments",
            values=["All Departments"],
            size_hint=(None, None),
            size=(170, 42),
            background_color=get_color_from_hex(Settings.COLOR_SURFACE),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        self.spn_dept.bind(text=lambda instance, text: self.perform_search())
        filter_bar.add_widget(self.spn_dept)

        # Status Spinner
        self.spn_status = Spinner(
            text="All Status",
            values=["All Status", "Active", "Inactive", "Suspended", "Graduated"],
            size_hint=(None, None),
            size=(110, 42),
            background_color=get_color_from_hex(Settings.COLOR_SURFACE),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        self.spn_status.bind(text=lambda instance, text: self.perform_search())
        filter_bar.add_widget(self.spn_status)

        # Search Button
        btn_search = Button(
            text="Search",
            bold=True,
            font_size="12sp",
            size_hint=(None, None),
            size=(80, 42),
            background_color=get_color_from_hex(Settings.COLOR_PRIMARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_search.bind(on_release=lambda x: self.perform_search())
        filter_bar.add_widget(btn_search)

        # Reset Filters Button
        btn_reset = Button(
            text="Reset",
            font_size="12sp",
            size_hint=(None, None),
            size=(70, 42),
            background_color=get_color_from_hex(Settings.COLOR_BORDER),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        btn_reset.bind(on_release=lambda x: self.reset_filters())
        filter_bar.add_widget(btn_reset)

        root.add_widget(filter_bar)

        # Status results count bar
        self.lbl_count = Label(
            text="Loading student directory...",
            font_size="12sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_y=None,
            height=20,
            halign="left",
            valign="middle",
        )
        self.lbl_count.bind(size=self.lbl_count.setter("text_size"))
        root.add_widget(self.lbl_count)

        # Scrollable student cards list
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.list_container = BoxLayout(orientation="vertical", spacing=8, size_hint_y=None)
        self.list_container.bind(minimum_height=self.list_container.setter("height"))
        scroll.add_widget(self.list_container)

        root.add_widget(scroll)
        self.add_widget(root)

    def on_enter(self) -> None:
        """Loads departments and triggers search when screen is displayed."""
        self.load_departments()
        self.perform_search()

    def load_departments(self) -> None:
        """Populates the department filter spinner."""
        depts = self.department_service.get_all()
        self.department_map = {"All Departments": 0}
        dept_names = ["All Departments"]
        for d in depts:
            self.department_map[d.name] = d.id
            dept_names.append(d.name)
        self.spn_dept.values = dept_names

    def reset_filters(self) -> None:
        """Clears search input and resets all dropdowns."""
        self.txt_search.text = ""
        self.spn_dept.text = "All Departments"
        self.spn_status.text = "All Status"
        self.perform_search()

    def perform_search(self) -> None:
        """Executes filtered student query and populates the list."""
        term = self.txt_search.text.strip()
        dept_name = self.spn_dept.text
        dept_id = self.department_map.get(dept_name, 0)
        status = self.spn_status.text if self.spn_status.text != "All Status" else "All"

        students = self.student_service.search(query_text=term, department_id=dept_id, status=status)

        self.list_container.clear_widgets()
        self.lbl_count.text = f"Showing {len(students)} student record(s)"

        if not students:
            empty_box = BoxLayout(orientation="vertical", size_hint_y=None, height=120, padding=20)
            lbl_empty = Label(
                text="No matching students found.\nTry adjusting your search criteria or register a new student.",
                font_size="13sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                halign="center",
                valign="middle",
            )
            lbl_empty.bind(size=lbl_empty.setter("text_size"))
            empty_box.add_widget(lbl_empty)
            self.list_container.add_widget(empty_box)
            return

        for student in students:
            card = StudentListItem(
                student=student,
                on_view=self.handle_view,
                on_edit=self.handle_edit,
                on_delete=self.handle_delete,
            )
            self.list_container.add_widget(card)

    def handle_view(self, student: Student) -> None:
        """Navigates to dedicated student details screen."""
        self.switch_screen("student_details", student.id)

    def handle_edit(self, student: Student) -> None:
        """Navigates to student form in edit mode."""
        self.switch_screen("student_form", student.id)

    def handle_delete(self, student: Student) -> None:
        """Displays confirmation dialog before deleting record."""
        def confirm_action():
            ok, msg = self.student_service.delete(student.id)  # type: ignore
            if ok:
                InfoDialog("Record Deleted", f"Student '{student.full_name}' was removed successfully.").open()
                self.perform_search()
            else:
                InfoDialog("Delete Failed", msg, is_error=True).open()

        ConfirmDialog(
            title="Delete Student Record",
            message=f"Are you sure you want to permanently delete\n{student.full_name} ({student.admission_number})?\n\nThis will remove attendance and marks records.",
            confirm_text="Delete Student",
            destructive=True,
            on_confirm=confirm_action,
        ).open()
