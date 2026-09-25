"""
Student registration and edit form screen.
Handles both addition of new students and updating existing profiles with
thorough client-side and database-level validation.
"""

from typing import Any, Dict, Optional
from datetime import date
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
from app.models.student import Student
from app.services.student_service import StudentService
from app.services.department_service import DepartmentService
from app.widgets.dialogs import InfoDialog
from app.utils.constants import GENDERS, STUDENT_STATUSES, ACADEMIC_YEARS


class StudentFormScreen(Screen):
    """
    Form view for Adding and Editing student profiles.
    """

    def __init__(self, switch_screen_cb, **kwargs) -> None:
        super().__init__(**kwargs)
        self.switch_screen = switch_screen_cb
        self.student_service = StudentService()
        self.department_service = DepartmentService()
        self.editing_student_id: Optional[int] = None
        self.department_map = {}

        # Root layout
        root = BoxLayout(orientation="vertical", spacing=10, padding=[20, 16, 20, 16])

        # Header with back button
        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)
        btn_back = Button(
            text="← Back to Directory",
            font_size="12sp",
            size_hint=(None, None),
            size=(140, 36),
            background_color=get_color_from_hex(Settings.COLOR_BORDER),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        btn_back.bind(on_release=lambda x: self.switch_screen("students"))
        header.add_widget(btn_back)

        self.lbl_title = Label(
            text="Register New Student",
            font_size="20sp",
            bold=True,
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_x=1,
            halign="left",
            valign="middle",
        )
        self.lbl_title.bind(size=self.lbl_title.setter("text_size"))
        header.add_widget(self.lbl_title)
        root.add_widget(header)

        # Validation message bar
        self.lbl_error = Label(
            text="",
            font_size="12sp",
            bold=True,
            color=get_color_from_hex(Settings.COLOR_ERROR),
            size_hint_y=None,
            height=20,
            halign="left",
            valign="middle",
        )
        self.lbl_error.bind(size=self.lbl_error.setter("text_size"))
        root.add_widget(self.lbl_error)

        # Scrollable form container
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        form_box = BoxLayout(orientation="vertical", spacing=14, size_hint_y=None, padding=[4, 4, 4, 16])
        form_box.bind(minimum_height=form_box.setter("height"))

        # Section 1: Academic & Identification
        form_box.add_widget(self._create_section_label("1. Academic & Enrollment Information"))
        grid_academic = GridLayout(cols=2, spacing=12, size_hint_y=None, height=130)

        # Admission Number
        self.inp_admission = self._create_text_input("e.g. ADM-2024-001")
        grid_academic.add_widget(self._wrap_field("Admission Number *", self.inp_admission))

        # Department Spinner
        self.spn_department = Spinner(
            text="Select Department",
            values=["Select Department"],
            size_hint_y=None,
            height=40,
            background_color=get_color_from_hex(Settings.COLOR_SURFACE),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        grid_academic.add_widget(self._wrap_field("Department / Class *", self.spn_department))

        # Academic Year
        self.spn_year = Spinner(
            text="1",
            values=[str(y) for y in ACADEMIC_YEARS],
            size_hint_y=None,
            height=40,
            background_color=get_color_from_hex(Settings.COLOR_SURFACE),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        grid_academic.add_widget(self._wrap_field("Current Year (1-4) *", self.spn_year))

        # Admission Date
        self.inp_admission_date = self._create_text_input("YYYY-MM-DD", default_val=str(date.today()))
        grid_academic.add_widget(self._wrap_field("Admission Date (YYYY-MM-DD) *", self.inp_admission_date))

        form_box.add_widget(grid_academic)

        # Section 2: Personal Details
        form_box.add_widget(self._create_section_label("2. Personal Information"))
        grid_personal = GridLayout(cols=2, spacing=12, size_hint_y=None, height=130)

        # First Name
        self.inp_first_name = self._create_text_input("First Name")
        grid_personal.add_widget(self._wrap_field("First Name *", self.inp_first_name))

        # Last Name
        self.inp_last_name = self._create_text_input("Last Name")
        grid_personal.add_widget(self._wrap_field("Last Name *", self.inp_last_name))

        # Gender
        self.spn_gender = Spinner(
            text="Male",
            values=list(GENDERS),
            size_hint_y=None,
            height=40,
            background_color=get_color_from_hex(Settings.COLOR_SURFACE),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        grid_personal.add_widget(self._wrap_field("Gender *", self.spn_gender))

        # Date of Birth
        self.inp_dob = self._create_text_input("YYYY-MM-DD (e.g. 2004-05-15)")
        grid_personal.add_widget(self._wrap_field("Date of Birth (YYYY-MM-DD) *", self.inp_dob))

        form_box.add_widget(grid_personal)

        # Section 3: Contact & Address
        form_box.add_widget(self._create_section_label("3. Student Contact & Residence"))
        grid_contact = GridLayout(cols=2, spacing=12, size_hint_y=None, height=130)

        # Email
        self.inp_email = self._create_text_input("student@example.com")
        grid_contact.add_widget(self._wrap_field("Email Address *", self.inp_email))

        # Phone
        self.inp_phone = self._create_text_input("+1-555-0100")
        grid_contact.add_widget(self._wrap_field("Phone Number *", self.inp_phone))

        # Status
        self.spn_status = Spinner(
            text="Active",
            values=list(STUDENT_STATUSES),
            size_hint_y=None,
            height=40,
            background_color=get_color_from_hex(Settings.COLOR_SURFACE),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        grid_contact.add_widget(self._wrap_field("Student Status *", self.spn_status))

        # Residential Address
        self.inp_address = self._create_text_input("Residential Street Address")
        grid_contact.add_widget(self._wrap_field("Residential Address *", self.inp_address))

        form_box.add_widget(grid_contact)

        # Section 4: Guardian Information
        form_box.add_widget(self._create_section_label("4. Guardian / Emergency Contact"))
        grid_guardian = GridLayout(cols=2, spacing=12, size_hint_y=None, height=65)

        self.inp_guardian_name = self._create_text_input("Parent or Guardian Full Name")
        grid_guardian.add_widget(self._wrap_field("Guardian Name *", self.inp_guardian_name))

        self.inp_guardian_phone = self._create_text_input("+1-555-0199")
        grid_guardian.add_widget(self._wrap_field("Guardian Phone Number *", self.inp_guardian_phone))

        form_box.add_widget(grid_guardian)

        # Action Buttons: Save & Reset
        action_row = BoxLayout(orientation="horizontal", spacing=12, size_hint_y=None, height=44, padding=[0, 10, 0, 0])

        btn_save = Button(
            text="Save Student Record",
            bold=True,
            font_size="13sp",
            size_hint=(None, None),
            size=(180, 42),
            background_color=get_color_from_hex(Settings.COLOR_PRIMARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_save.bind(on_release=lambda x: self.save_student())
        action_row.add_widget(btn_save)

        btn_clear = Button(
            text="Reset Form",
            font_size="13sp",
            size_hint=(None, None),
            size=(110, 42),
            background_color=get_color_from_hex(Settings.COLOR_BORDER),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        btn_clear.bind(on_release=lambda x: self.reset_form())
        action_row.add_widget(btn_clear)

        form_box.add_widget(action_row)
        scroll.add_widget(form_box)
        root.add_widget(scroll)

        self.add_widget(root)

    def _create_section_label(self, text: str) -> Label:
        lbl = Label(
            text=text,
            bold=True,
            font_size="14sp",
            color=get_color_from_hex(Settings.COLOR_PRIMARY),
            size_hint_y=None,
            height=26,
            halign="left",
            valign="middle",
        )
        lbl.bind(size=lbl.setter("text_size"))
        return lbl

    def _create_text_input(self, hint: str, default_val: str = "") -> TextInput:
        return TextInput(
            text=default_val,
            hint_text=hint,
            multiline=False,
            font_size="13sp",
            size_hint_y=None,
            height=40,
            padding=[10, 10, 10, 10],
            background_color=get_color_from_hex(Settings.COLOR_SURFACE),
            foreground_color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )

    def _wrap_field(self, label_text: str, widget: Any) -> BoxLayout:
        box = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None, height=60)
        lbl = Label(
            text=label_text,
            font_size="11sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_y=None,
            height=16,
            halign="left",
            valign="middle",
        )
        lbl.bind(size=lbl.setter("text_size"))
        box.add_widget(lbl)
        box.add_widget(widget)
        return box

    def set_editing_student(self, student_id: Optional[int]) -> None:
        """Configures form for Add mode or Edit mode."""
        self.load_departments()
        self.lbl_error.text = ""
        self.editing_student_id = student_id

        if student_id:
            self.lbl_title.text = "Edit Student Profile"
            st = self.student_service.get_by_id(student_id)
            if st:
                self.inp_admission.text = st.admission_number
                self.inp_first_name.text = st.first_name
                self.inp_last_name.text = st.last_name
                self.spn_gender.text = st.gender
                self.inp_dob.text = str(st.date_of_birth)
                self.inp_phone.text = st.phone_number
                self.inp_email.text = st.email
                self.inp_address.text = st.address
                self.spn_year.text = str(st.year)
                self.inp_guardian_name.text = st.guardian_name
                self.inp_guardian_phone.text = st.guardian_phone
                self.inp_admission_date.text = str(st.admission_date)
                self.spn_status.text = st.status

                # Find department name
                for name, d_id in self.department_map.items():
                    if d_id == st.department_id:
                        self.spn_department.text = name
                        break
        else:
            self.lbl_title.text = "Register New Student"
            self.reset_form()

    def load_departments(self) -> None:
        """Loads available departments into the dropdown."""
        depts = self.department_service.get_active()
        self.department_map = {}
        names = []
        for d in depts:
            self.department_map[d.name] = d.id
            names.append(d.name)
        self.spn_department.values = names
        if names and self.spn_department.text == "Select Department":
            self.spn_department.text = names[0]

    def reset_form(self) -> None:
        """Clears all inputs back to pristine defaults."""
        self.inp_admission.text = ""
        self.inp_first_name.text = ""
        self.inp_last_name.text = ""
        self.spn_gender.text = "Male"
        self.inp_dob.text = ""
        self.inp_phone.text = ""
        self.inp_email.text = ""
        self.inp_address.text = ""
        self.spn_year.text = "1"
        self.inp_guardian_name.text = ""
        self.inp_guardian_phone.text = ""
        self.inp_admission_date.text = str(date.today())
        self.spn_status.text = "Active"
        self.lbl_error.text = ""
        if self.spn_department.values:
            self.spn_department.text = self.spn_department.values[0]

    def save_student(self) -> None:
        """Validates payload and submits insert or update operation."""
        dept_name = self.spn_department.text
        dept_id = self.department_map.get(dept_name, 0)

        data = {
            "admission_number": self.inp_admission.text.strip(),
            "first_name": self.inp_first_name.text.strip(),
            "last_name": self.inp_last_name.text.strip(),
            "gender": self.spn_gender.text,
            "date_of_birth": self.inp_dob.text.strip(),
            "phone_number": self.inp_phone.text.strip(),
            "email": self.inp_email.text.strip(),
            "address": self.inp_address.text.strip(),
            "department_id": dept_id,
            "year": int(self.spn_year.text),
            "guardian_name": self.inp_guardian_name.text.strip(),
            "guardian_phone": self.inp_guardian_phone.text.strip(),
            "admission_date": self.inp_admission_date.text.strip(),
            "status": self.spn_status.text,
        }

        if self.editing_student_id:
            ok, msg = self.student_service.update(self.editing_student_id, data)
            if ok:
                InfoDialog(
                    "Profile Updated",
                    f"Student {data['first_name']} {data['last_name']} updated successfully.",
                    on_close=lambda: self.switch_screen("student_details", self.editing_student_id),
                ).open()
            else:
                self.lbl_error.text = msg
        else:
            ok, msg, new_id = self.student_service.create(data)
            if ok:
                InfoDialog(
                    "Registration Successful",
                    f"Student {data['first_name']} {data['last_name']} registered successfully.",
                    on_close=lambda: self.switch_screen("student_details", new_id),
                ).open()
            else:
                self.lbl_error.text = msg
