"""
Department and class administration screen.
Manages academic divisions, student enrollment headcounts, and status toggles.
"""

from typing import Optional
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
from app.models.department import Department
from app.services.department_service import DepartmentService
from app.widgets.dialogs import ConfirmDialog, InfoDialog


class DepartmentsScreen(Screen):
    """
    Department management screen.
    """

    def __init__(self, switch_screen_cb, **kwargs) -> None:
        super().__init__(**kwargs)
        self.switch_screen = switch_screen_cb
        self.department_service = DepartmentService()
        self.editing_dept_id: Optional[int] = None

        # Main layout
        root = BoxLayout(orientation="vertical", spacing=12, padding=[20, 16, 20, 16])

        # Header Title
        title_box = BoxLayout(orientation="vertical", size_hint_y=None, height=44, spacing=2)
        title_lbl = Label(
            text="Academic Departments & Classes",
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
            text="Organize curriculum programs and maintain enrollment relationships",
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

        # Department Creation / Edit Card
        card = BoxLayout(orientation="vertical", size_hint_y=None, height=170, padding=16, spacing=10)
        with card.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_SURFACE))
            card.bg = RoundedRectangle(pos=card.pos, size=card.size, radius=[6, 6, 6, 6])
            Color(*get_color_from_hex(Settings.COLOR_BORDER))
            card.line = Line(rounded_rectangle=[card.x, card.y, card.width, card.height, 6], width=1)

        def _upd_c(ins, *args):
            ins.bg.pos = ins.pos
            ins.bg.size = ins.size
            ins.line.rounded_rectangle = [ins.x, ins.y, ins.width, ins.height, 6]

        card.bind(pos=_upd_c, size=_upd_c)

        self.lbl_form_title = Label(
            text="Add New Department",
            bold=True,
            font_size="14sp",
            color=get_color_from_hex(Settings.COLOR_PRIMARY),
            size_hint_y=None,
            height=20,
            halign="left",
            valign="middle",
        )
        self.lbl_form_title.bind(size=self.lbl_form_title.setter("text_size"))
        card.add_widget(self.lbl_form_title)

        # Inputs row
        row_inp = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=40)

        self.inp_code = TextInput(
            hint_text="Code (e.g. CS)",
            multiline=False,
            size_hint_x=0.20,
            font_size="13sp",
            padding=[8, 8, 8, 8],
            background_color=get_color_from_hex(Settings.COLOR_BACKGROUND),
            foreground_color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        row_inp.add_widget(self.inp_code)

        self.inp_name = TextInput(
            hint_text="Department Name (e.g. Computer Science)",
            multiline=False,
            size_hint_x=0.45,
            font_size="13sp",
            padding=[8, 8, 8, 8],
            background_color=get_color_from_hex(Settings.COLOR_BACKGROUND),
            foreground_color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        row_inp.add_widget(self.inp_name)

        self.spn_status = Spinner(
            text="Active",
            values=["Active", "Inactive"],
            size_hint_x=0.20,
            background_color=get_color_from_hex(Settings.COLOR_BACKGROUND),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        row_inp.add_widget(self.spn_status)

        # Save Button
        btn_save = Button(
            text="Save Department",
            bold=True,
            font_size="12sp",
            size_hint_x=0.25,
            background_color=get_color_from_hex(Settings.COLOR_PRIMARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_save.bind(on_release=lambda x: self.save_department())
        row_inp.add_widget(btn_save)

        btn_cancel = Button(
            text="Reset",
            font_size="12sp",
            size_hint_x=0.15,
            background_color=get_color_from_hex(Settings.COLOR_BORDER),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        btn_cancel.bind(on_release=lambda x: self.reset_form())
        row_inp.add_widget(btn_cancel)

        card.add_widget(row_inp)

        # Description row
        self.inp_desc = TextInput(
            hint_text="Description or syllabus overview (optional)",
            multiline=False,
            size_hint_y=None,
            height=36,
            font_size="12sp",
            padding=[8, 8, 8, 8],
            background_color=get_color_from_hex(Settings.COLOR_BACKGROUND),
            foreground_color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        card.add_widget(self.inp_desc)

        root.add_widget(card)

        # Table Header
        tbl_hdr = BoxLayout(orientation="horizontal", size_hint_y=None, height=34, padding=[14, 4, 14, 4], spacing=10)
        with tbl_hdr.canvas.before:
            Color(*get_color_from_hex("#E2E8F0"))
            tbl_hdr.bg = RoundedRectangle(pos=tbl_hdr.pos, size=tbl_hdr.size, radius=[4, 4, 0, 0])

        def _upd_th(ins, *args):
            ins.bg.pos = ins.pos
            ins.bg.size = ins.size

        tbl_hdr.bind(pos=_upd_th, size=_upd_th)

        tbl_hdr.add_widget(self._cell_hdr("Code", width=80))
        tbl_hdr.add_widget(self._cell_hdr("Department Name", flex=1))
        tbl_hdr.add_widget(self._cell_hdr("Description", flex=2))
        tbl_hdr.add_widget(self._cell_hdr("Students Enrolled", width=130))
        tbl_hdr.add_widget(self._cell_hdr("Status", width=90))
        tbl_hdr.add_widget(self._cell_hdr("Actions", width=140))
        root.add_widget(tbl_hdr)

        # Scrollable Department List
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.dept_list_box = BoxLayout(orientation="vertical", spacing=4, size_hint_y=None)
        self.dept_list_box.bind(minimum_height=self.dept_list_box.setter("height"))

        scroll.add_widget(self.dept_list_box)
        root.add_widget(scroll)
        self.add_widget(root)

    def _cell_hdr(self, text: str, width: Optional[int] = None, flex: Optional[int] = None) -> Label:
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
        """Loads departments on entry."""
        self.load_departments()

    def reset_form(self) -> None:
        """Resets the department form."""
        self.editing_dept_id = None
        self.lbl_form_title.text = "Add New Department"
        self.inp_code.text = ""
        self.inp_name.text = ""
        self.inp_desc.text = ""
        self.spn_status.text = "Active"

    def load_departments(self) -> None:
        """Fetches and displays departments."""
        depts = self.department_service.get_all()
        self.dept_list_box.clear_widgets()

        if not depts:
            lbl_empty = Label(
                text="No departments found. Use the form above to add a department.",
                font_size="13sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                size_hint_y=None,
                height=50,
            )
            self.dept_list_box.add_widget(lbl_empty)
            return

        for d in depts:
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=44, padding=[14, 6, 14, 6], spacing=10)
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

            # Code
            c_lbl = Label(
                text=d.code,
                bold=True,
                font_size="11sp",
                color=get_color_from_hex(Settings.COLOR_PRIMARY),
                size_hint_x=None,
                width=80,
                halign="left",
                valign="middle",
            )
            c_lbl.bind(size=c_lbl.setter("text_size"))
            row.add_widget(c_lbl)

            # Name
            n_lbl = Label(
                text=d.name,
                bold=True,
                font_size="12sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
                size_hint_x=1,
                halign="left",
                valign="middle",
            )
            n_lbl.bind(size=n_lbl.setter("text_size"))
            row.add_widget(n_lbl)

            # Description
            desc_lbl = Label(
                text=d.description[:60] + ("..." if len(d.description) > 60 else ""),
                font_size="11sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                size_hint_x=2,
                halign="left",
                valign="middle",
            )
            desc_lbl.bind(size=desc_lbl.setter("text_size"))
            row.add_widget(desc_lbl)

            # Student Count
            cnt_lbl = Label(
                text=f"{d.student_count} student(s)",
                font_size="11sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                size_hint_x=None,
                width=130,
                halign="left",
                valign="middle",
            )
            cnt_lbl.bind(size=cnt_lbl.setter("text_size"))
            row.add_widget(cnt_lbl)

            # Status
            stat_color = Settings.COLOR_SUCCESS if d.status == "Active" else Settings.COLOR_ERROR
            stat_lbl = Label(
                text=d.status,
                bold=True,
                font_size="11sp",
                color=get_color_from_hex(stat_color),
                size_hint_x=None,
                width=90,
                halign="left",
                valign="middle",
            )
            stat_lbl.bind(size=stat_lbl.setter("text_size"))
            row.add_widget(stat_lbl)

            # Actions
            act_box = BoxLayout(orientation="horizontal", size_hint_x=None, width=140, spacing=6)

            btn_edit = Button(
                text="Edit",
                font_size="10sp",
                size_hint=(None, None),
                size=(60, 28),
                background_color=get_color_from_hex(Settings.COLOR_SECONDARY),
                color=get_color_from_hex("#FFFFFF"),
            )
            btn_edit.bind(on_release=lambda x, dept=d: self.edit_department(dept))
            act_box.add_widget(btn_edit)

            btn_del = Button(
                text="Delete",
                font_size="10sp",
                size_hint=(None, None),
                size=(60, 28),
                background_color=get_color_from_hex(Settings.COLOR_ERROR),
                color=get_color_from_hex("#FFFFFF"),
            )
            btn_del.bind(on_release=lambda x, dept=d: self.delete_department(dept))
            act_box.add_widget(btn_del)

            row.add_widget(act_box)
            self.dept_list_box.add_widget(row)

    def edit_department(self, dept: Department) -> None:
        """Populates form with department to edit."""
        self.editing_dept_id = dept.id
        self.lbl_form_title.text = f"Edit Department: {dept.name}"
        self.inp_code.text = dept.code
        self.inp_name.text = dept.name
        self.inp_desc.text = dept.description
        self.spn_status.text = dept.status

    def delete_department(self, dept: Department) -> None:
        """Deletes department after validation."""
        def confirm():
            ok, msg = self.department_service.delete(dept.id)  # type: ignore
            if ok:
                self.load_departments()
                InfoDialog("Success", "Department deleted.").open()
            else:
                InfoDialog("Cannot Delete", msg, is_error=True).open()

        ConfirmDialog(
            title="Delete Department",
            message=f"Are you sure you want to delete '{dept.name}' ({dept.code})?",
            on_confirm=confirm,
        ).open()

    def save_department(self) -> None:
        """Saves new or edited department."""
        code = self.inp_code.text.strip()
        name = self.inp_name.text.strip()
        desc = self.inp_desc.text.strip()
        status = self.spn_status.text

        if self.editing_dept_id:
            ok, msg = self.department_service.update(self.editing_dept_id, code, name, desc, status)
        else:
            ok, msg, _ = self.department_service.create(code, name, desc, status)

        if ok:
            self.reset_form()
            self.load_departments()
            InfoDialog("Success", msg).open()
        else:
            InfoDialog("Validation Error", msg, is_error=True).open()
