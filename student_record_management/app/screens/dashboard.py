"""
Administrative dashboard screen.
Displays real-time institutional metrics, gender ratios, recent student enrollments,
and quick administrative action shortcuts.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex

from app.config.settings import Settings
from app.services.student_service import StudentService
from app.widgets.statistic_card import StatisticCard


class DashboardScreen(Screen):
    """
    Overview executive screen for academic administrators.
    """

    def __init__(self, switch_screen_cb, **kwargs) -> None:
        super().__init__(**kwargs)
        self.switch_screen = switch_screen_cb
        self.student_service = StudentService()

        # Main vertical container with soft background
        root_box = BoxLayout(orientation="vertical", spacing=14, padding=[20, 16, 20, 16])

        # Page Title & Welcome Banner
        title_box = BoxLayout(orientation="vertical", size_hint_y=None, height=54, spacing=2)
        title_lbl = Label(
            text="ScholarPulse Dashboard",
            font_size="22sp",
            bold=True,
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_y=None,
            height=30,
            halign="left",
            valign="middle",
        )
        title_lbl.bind(size=title_lbl.setter("text_size"))
        title_box.add_widget(title_lbl)

        sub_lbl = Label(
            text="Real-time academic performance, enrollment metrics & registry overview",
            font_size="13sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_y=None,
            height=20,
            halign="left",
            valign="middle",
        )
        sub_lbl.bind(size=sub_lbl.setter("text_size"))
        title_box.add_widget(sub_lbl)
        root_box.add_widget(title_box)

        # Quick Actions Action Bar
        action_bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, spacing=10)

        btn_add = Button(
            text="+ Add Student",
            bold=True,
            font_size="12sp",
            size_hint_x=None,
            width=130,
            background_color=get_color_from_hex(Settings.COLOR_PRIMARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_add.bind(on_release=lambda x: self.switch_screen("student_form", None))
        action_bar.add_widget(btn_add)

        btn_att = Button(
            text="Mark Attendance",
            font_size="12sp",
            size_hint_x=None,
            width=140,
            background_color=get_color_from_hex(Settings.COLOR_SECONDARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_att.bind(on_release=lambda x: self.switch_screen("attendance"))
        action_bar.add_widget(btn_att)

        btn_rep = Button(
            text="Generate Reports",
            font_size="12sp",
            size_hint_x=None,
            width=140,
            background_color=get_color_from_hex("#475569"),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_rep.bind(on_release=lambda x: self.switch_screen("reports"))
        action_bar.add_widget(btn_rep)

        action_bar.add_widget(Label(size_hint_x=1))  # Spacer
        root_box.add_widget(action_bar)

        # Scrollable content area
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        content_box = BoxLayout(orientation="vertical", spacing=18, size_hint_y=None)
        content_box.bind(minimum_height=content_box.setter("height"))

        # 1. Summary Cards Grid
        self.kpi_grid = GridLayout(cols=4, spacing=12, size_hint_y=None, height=120)

        self.card_total = StatisticCard("Total Students", "0", "All Enrolled", accent_color=Settings.COLOR_PRIMARY)
        self.card_active = StatisticCard("Active Students", "0", "Good Standing", accent_color=Settings.COLOR_SUCCESS)
        self.card_gender = StatisticCard("Gender Distribution", "0M / 0F", "Male / Female ratio", accent_color=Settings.COLOR_SECONDARY)
        self.card_dept = StatisticCard("Departments", "0", "Active faculties", accent_color="#6366F1")

        self.kpi_grid.add_widget(self.card_total)
        self.kpi_grid.add_widget(self.card_active)
        self.kpi_grid.add_widget(self.card_gender)
        self.kpi_grid.add_widget(self.card_dept)
        content_box.add_widget(self.kpi_grid)

        # 2. Recently Registered Students Section
        recent_section = BoxLayout(orientation="vertical", spacing=10, size_hint_y=None, height=330)

        recent_header = BoxLayout(orientation="horizontal", size_hint_y=None, height=30)
        recent_title = Label(
            text="Recently Registered Students",
            bold=True,
            font_size="16sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_x=1,
            halign="left",
            valign="middle",
        )
        recent_title.bind(size=recent_title.setter("text_size"))
        recent_header.add_widget(recent_title)

        btn_view_all = Button(
            text="View Full Directory →",
            font_size="12sp",
            size_hint_x=None,
            width=160,
            background_color=get_color_from_hex(Settings.COLOR_BACKGROUND),
            color=get_color_from_hex(Settings.COLOR_PRIMARY_LIGHT),
        )
        btn_view_all.bind(on_release=lambda x: self.switch_screen("students"))
        recent_header.add_widget(btn_view_all)
        recent_section.add_widget(recent_header)

        # Container for student list
        self.recent_container = BoxLayout(orientation="vertical", spacing=6, size_hint_y=None)
        self.recent_container.bind(minimum_height=self.recent_container.setter("height"))
        recent_section.add_widget(self.recent_container)

        content_box.add_widget(recent_section)
        scroll.add_widget(content_box)
        root_box.add_widget(scroll)

        self.add_widget(root_box)

    def on_enter(self) -> None:
        """Reloads metrics and recent students on entering screen."""
        self.refresh_data()

    def refresh_data(self) -> None:
        """Fetches fresh metrics from StudentService."""
        data = self.student_service.get_dashboard_metrics()

        tot = data.get("total_students", 0)
        act = data.get("active_students", 0)
        male = data.get("male_students", 0)
        fem = data.get("female_students", 0)
        depts = data.get("total_departments", 0)

        self.card_total.update_value(str(tot), f"{act} currently active")
        self.card_active.update_value(str(act), f"{(act/tot*100):.1f}% active rate" if tot else "0%")
        self.card_gender.update_value(f"{male}M / {fem}F", f"{male} Male, {fem} Female")
        self.card_dept.update_value(str(depts), "Academic divisions")

        # Update recent list
        self.recent_container.clear_widgets()
        recent_students = data.get("recent_students", [])

        if not recent_students:
            empty_lbl = Label(
                text="No student records added yet. Click '+ Add Student' above to get started.",
                font_size="13sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                size_hint_y=None,
                height=50,
            )
            self.recent_container.add_widget(empty_lbl)
            return

        for st in recent_students:
            row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=48,
                padding=[12, 8, 12, 8],
                spacing=10,
            )
            with row.canvas.before:
                Color(*get_color_from_hex(Settings.COLOR_SURFACE))
                row.bg = RoundedRectangle(pos=row.pos, size=row.size, radius=[4, 4, 4, 4])
                Color(*get_color_from_hex(Settings.COLOR_BORDER))
                row.line = Line(rounded_rectangle=[row.x, row.y, row.width, row.height, 4], width=1)

            def _update_row_rects(instance, *args):
                instance.bg.pos = instance.pos
                instance.bg.size = instance.size
                instance.line.rounded_rectangle = [instance.x, instance.y, instance.width, instance.height, 4]

            row.bind(pos=_update_row_rects, size=_update_row_rects)

            adm_lbl = Label(
                text=st.admission_number,
                bold=True,
                font_size="12sp",
                color=get_color_from_hex(Settings.COLOR_PRIMARY),
                size_hint_x=None,
                width=110,
                halign="left",
                valign="middle",
            )
            adm_lbl.bind(size=adm_lbl.setter("text_size"))
            row.add_widget(adm_lbl)

            name_lbl = Label(
                text=st.full_name,
                bold=True,
                font_size="13sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
                size_hint_x=1,
                halign="left",
                valign="middle",
            )
            name_lbl.bind(size=name_lbl.setter("text_size"))
            row.add_widget(name_lbl)

            dept_lbl = Label(
                text=f"{st.department_name} (Yr {st.year})",
                font_size="12sp",
                color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
                size_hint_x=None,
                width=200,
                halign="left",
                valign="middle",
            )
            dept_lbl.bind(size=dept_lbl.setter("text_size"))
            row.add_widget(dept_lbl)

            btn_open = Button(
                text="View",
                font_size="11sp",
                size_hint=(None, None),
                size=(60, 28),
                background_color=get_color_from_hex(Settings.COLOR_PRIMARY),
                color=get_color_from_hex("#FFFFFF"),
            )
            btn_open.bind(on_release=lambda x, s=st: self.switch_screen("student_details", s.id))
            row.add_widget(btn_open)

            self.recent_container.add_widget(row)
