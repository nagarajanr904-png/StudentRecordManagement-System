"""
Reports and audit documents generation screen.
Compiles official PDF student directories using ReportLab and exports CSV
spreadsheets for attendance and examination marks.
"""

from datetime import date
from pathlib import Path
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex

from app.config.settings import Settings, BASE_DIR
from app.services.report_service import ReportService
from app.widgets.dialogs import InfoDialog


class ReportsScreen(Screen):
    """
    Administrative reporting center.
    """

    def __init__(self, switch_screen_cb, **kwargs) -> None:
        super().__init__(**kwargs)
        self.switch_screen = switch_screen_cb
        self.report_service = ReportService()

        # Output directory
        self.export_dir = BASE_DIR / "reports_export"
        self.export_dir.mkdir(parents=True, exist_ok=True)

        # Main layout
        root = BoxLayout(orientation="vertical", spacing=14, padding=[20, 16, 20, 16])

        # Header Title
        title_box = BoxLayout(orientation="vertical", size_hint_y=None, height=44, spacing=2)
        title_lbl = Label(
            text="Reports & Data Export Center",
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
            text="Generate printable institutional PDFs and spreadsheet exports for record keeping",
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

        # Reports Grid
        grid = GridLayout(cols=2, spacing=14, size_hint_y=None, height=420)

        # Card 1: Official Student Directory (PDF)
        grid.add_widget(
            self._create_report_card(
                title="Official Student Directory (PDF)",
                desc="Formal landscape PDF publication formatted with institutional headers, page numbers, and complete student rosters.",
                btn_text="Generate PDF Report",
                on_click=self.generate_student_pdf,
                badge="PDF Format",
                badge_color=Settings.COLOR_PRIMARY,
            )
        )

        # Card 2: Student Registry Spreadsheet (CSV)
        grid.add_widget(
            self._create_report_card(
                title="Complete Student Registry (CSV)",
                desc="Raw tabular student dataset containing all enrollment fields, contact emails, addresses, and guardian information for Excel.",
                btn_text="Export Students CSV",
                on_click=self.generate_student_csv,
                badge="CSV Spreadsheet",
                badge_color=Settings.COLOR_SECONDARY,
            )
        )

        # Card 3: Daily Attendance Audit Log (CSV)
        att_card = BoxLayout(orientation="vertical", spacing=8, padding=16, size_hint_y=None, height=195)
        with att_card.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_SURFACE))
            att_card.bg = RoundedRectangle(pos=att_card.pos, size=att_card.size, radius=[6, 6, 6, 6])
            Color(*get_color_from_hex(Settings.COLOR_BORDER))
            att_card.line = Line(rounded_rectangle=[att_card.x, att_card.y, att_card.width, att_card.height, 6], width=1)

        def _upd_ac(ins, *args):
            ins.bg.pos = ins.pos
            ins.bg.size = ins.size
            ins.line.rounded_rectangle = [ins.x, ins.y, ins.width, ins.height, 6]

        att_card.bind(pos=_upd_ac, size=_upd_ac)

        att_title_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=22)
        att_title = Label(
            text="Attendance Audit Log (CSV)",
            bold=True,
            font_size="13sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_x=1,
            halign="left",
            valign="middle",
        )
        att_title.bind(size=att_title.setter("text_size"))
        att_title_row.add_widget(att_title)
        att_card.add_widget(att_title_row)

        att_desc = Label(
            text="Export presence and tardiness audit logs for a specific calendar date.",
            font_size="11sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_y=None,
            height=36,
            halign="left",
            valign="top",
        )
        att_desc.bind(size=att_desc.setter("text_size"))
        att_card.add_widget(att_desc)

        # Date input row
        date_row = BoxLayout(orientation="horizontal", spacing=8, size_hint_y=None, height=36)
        date_lbl = Label(
            text="Target Date:",
            font_size="11sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_x=None,
            width=80,
            halign="left",
            valign="middle",
        )
        date_lbl.bind(size=date_lbl.setter("text_size"))
        date_row.add_widget(date_lbl)

        self.inp_att_date = TextInput(
            text=str(date.today()),
            multiline=False,
            size_hint_x=1,
            font_size="12sp",
            padding=[6, 6, 6, 6],
            background_color=get_color_from_hex(Settings.COLOR_BACKGROUND),
            foreground_color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
        )
        date_row.add_widget(self.inp_att_date)
        att_card.add_widget(date_row)

        btn_att_export = Button(
            text="Export Attendance CSV",
            bold=True,
            font_size="12sp",
            size_hint_y=None,
            height=38,
            background_color=get_color_from_hex(Settings.COLOR_SECONDARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_att_export.bind(on_release=lambda x: self.generate_attendance_csv())
        att_card.add_widget(btn_att_export)

        grid.add_widget(att_card)

        # Card 4: Marks & Examination Transcript (CSV)
        grid.add_widget(
            self._create_report_card(
                title="Marks & Results Transcript (CSV)",
                desc="Comprehensive academic grading export with subjects, maximum scores, percentages, and computed letter grades.",
                btn_text="Export Examination CSV",
                on_click=self.generate_marks_csv,
                badge="CSV Spreadsheet",
                badge_color=Settings.COLOR_SECONDARY,
            )
        )

        root.add_widget(grid)

        # Output location path info box
        path_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=32, spacing=8)
        lbl_loc = Label(
            text=f"Exports saved to: {self.export_dir}",
            font_size="11sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_x=1,
            halign="left",
            valign="middle",
        )
        lbl_loc.bind(size=lbl_loc.setter("text_size"))
        path_box.add_widget(lbl_loc)
        root.add_widget(path_box)

        self.add_widget(root)

    def _create_report_card(self, title: str, desc: str, btn_text: str, on_click, badge: str, badge_color: str) -> BoxLayout:
        card = BoxLayout(orientation="vertical", spacing=8, padding=16, size_hint_y=None, height=195)
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

        top_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=22)
        t_lbl = Label(
            text=title,
            bold=True,
            font_size="13sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_x=1,
            halign="left",
            valign="middle",
        )
        t_lbl.bind(size=t_lbl.setter("text_size"))
        top_row.add_widget(t_lbl)

        badge_lbl = Label(
            text=badge,
            font_size="10sp",
            bold=True,
            color=get_color_from_hex(badge_color),
            size_hint_x=None,
            width=90,
            halign="right",
            valign="middle",
        )
        badge_lbl.bind(size=badge_lbl.setter("text_size"))
        top_row.add_widget(badge_lbl)
        card.add_widget(top_row)

        d_lbl = Label(
            text=desc,
            font_size="11sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_y=None,
            height=48,
            halign="left",
            valign="top",
        )
        d_lbl.bind(size=d_lbl.setter("text_size"))
        card.add_widget(d_lbl)

        btn = Button(
            text=btn_text,
            bold=True,
            font_size="12sp",
            size_hint_y=None,
            height=38,
            background_color=get_color_from_hex(badge_color),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn.bind(on_release=lambda x: on_click())
        card.add_widget(btn)

        return card

    def generate_student_pdf(self) -> None:
        filename = f"students_directory_{date.today().strftime('%Y%m%d')}.pdf"
        out_path = str(self.export_dir / filename)
        ok, msg = self.report_service.generate_students_pdf(out_path)
        InfoDialog("PDF Generation", msg, is_error=(not ok)).open()

    def generate_student_csv(self) -> None:
        filename = f"students_export_{date.today().strftime('%Y%m%d')}.csv"
        out_path = str(self.export_dir / filename)
        ok, msg = self.report_service.generate_students_csv(out_path)
        InfoDialog("CSV Export", msg, is_error=(not ok)).open()

    def generate_attendance_csv(self) -> None:
        target_date = self.inp_att_date.text.strip()
        filename = f"attendance_{target_date}.csv"
        out_path = str(self.export_dir / filename)
        ok, msg = self.report_service.generate_attendance_csv(out_path, target_date)
        InfoDialog("Attendance Export", msg, is_error=(not ok)).open()

    def generate_marks_csv(self) -> None:
        filename = f"marks_results_{date.today().strftime('%Y%m%d')}.csv"
        out_path = str(self.export_dir / filename)
        ok, msg = self.report_service.generate_marks_csv(out_path)
        InfoDialog("Marks Export", msg, is_error=(not ok)).open()
