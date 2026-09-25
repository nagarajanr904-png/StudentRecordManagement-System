"""
Database and system configuration screen.
Displays current connection status, connection testing tools, logging status,
and cloud database setup guidance.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex

from app.config.settings import Settings, LOG_FILE
from app.database.connection import get_db
from app.widgets.dialogs import InfoDialog


class SettingsScreen(Screen):
    """
    Database settings and connectivity diagnostic screen.
    """

    def __init__(self, switch_screen_cb, **kwargs) -> None:
        super().__init__(**kwargs)
        self.switch_screen = switch_screen_cb
        self.db = get_db()

        # Root layout
        root = BoxLayout(orientation="vertical", spacing=14, padding=[20, 16, 20, 16])

        # Header Title
        title_box = BoxLayout(orientation="vertical", size_hint_y=None, height=44, spacing=2)
        title_lbl = Label(
            text="Database & Environment Diagnostics",
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
            text="Inspect remote MySQL configuration, test latency, and view runtime diagnostic logs",
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

        # Scrollable content
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        box = BoxLayout(orientation="vertical", spacing=14, size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))

        # Connection Status Banner Card
        self.card_status = BoxLayout(orientation="vertical", spacing=8, padding=16, size_hint_y=None, height=140)
        with self.card_status.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_SURFACE))
            self.card_status.bg = RoundedRectangle(pos=self.card_status.pos, size=self.card_status.size, radius=[6, 6, 6, 6])
            Color(*get_color_from_hex(Settings.COLOR_BORDER))
            self.card_status.line = Line(rounded_rectangle=[self.card_status.x, self.card_status.y, self.card_status.width, self.card_status.height, 6], width=1)

        def _upd_cs(ins, *args):
            ins.bg.pos = ins.pos
            ins.bg.size = ins.size
            ins.line.rounded_rectangle = [ins.x, ins.y, ins.width, ins.height, 6]

        self.card_status.bind(pos=_upd_cs, size=_upd_cs)

        self.lbl_status_badge = Label(
            text="CONNECTION STATUS: CHECKING...",
            bold=True,
            font_size="13sp",
            size_hint_y=None,
            height=20,
            halign="left",
            valign="middle",
        )
        self.lbl_status_badge.bind(size=self.lbl_status_badge.setter("text_size"))
        self.card_status.add_widget(self.lbl_status_badge)

        self.lbl_status_detail = Label(
            text="",
            font_size="12sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_y=None,
            height=36,
            halign="left",
            valign="top",
        )
        self.lbl_status_detail.bind(size=self.lbl_status_detail.setter("text_size"))
        self.card_status.add_widget(self.lbl_status_detail)

        # Action row
        btn_row = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=36)

        btn_test = Button(
            text="Test Connection & Reconnect",
            bold=True,
            font_size="12sp",
            size_hint_x=None,
            width=220,
            background_color=get_color_from_hex(Settings.COLOR_PRIMARY),
            color=get_color_from_hex("#FFFFFF"),
        )
        btn_test.bind(on_release=lambda x: self.test_reconnect())
        btn_row.add_widget(btn_test)

        self.card_status.add_widget(btn_row)
        box.add_widget(self.card_status)

        # Configuration Parameters Grid
        grid_params = GridLayout(cols=2, spacing=12, size_hint_y=None, height=180)

        # Parameters Card
        p_card = BoxLayout(orientation="vertical", spacing=6, padding=16, size_hint_y=None, height=180)
        with p_card.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_SURFACE))
            p_card.bg = RoundedRectangle(pos=p_card.pos, size=p_card.size, radius=[6, 6, 6, 6])
            Color(*get_color_from_hex(Settings.COLOR_BORDER))
            p_card.line = Line(rounded_rectangle=[p_card.x, p_card.y, p_card.width, p_card.height, 6], width=1)

        p_card.bind(pos=_upd_cs, size=_upd_cs)

        p_title = Label(
            text="Active .env Parameters",
            bold=True,
            font_size="13sp",
            color=get_color_from_hex(Settings.COLOR_PRIMARY),
            size_hint_y=None,
            height=20,
            halign="left",
        )
        p_title.bind(size=p_title.setter("text_size"))
        p_card.add_widget(p_title)

        self.lbl_host = self._make_kv("Host (DB_HOST)", Settings.DB_HOST or "(Not set - Demo mode)")
        p_card.add_widget(self.lbl_host)

        self.lbl_port = self._make_kv("Port (DB_PORT)", str(Settings.DB_PORT))
        p_card.add_widget(self.lbl_port)

        self.lbl_db = self._make_kv("Database (DB_NAME)", Settings.DB_NAME or "(Not set)")
        p_card.add_widget(self.lbl_db)

        self.lbl_user = self._make_kv("Username (DB_USER)", Settings.DB_USER or "(Not set)")
        p_card.add_widget(self.lbl_user)

        self.lbl_pass = self._make_kv("Password (DB_PASSWORD)", "••••••••" if Settings.DB_PASSWORD else "(Not set)")
        p_card.add_widget(self.lbl_pass)

        grid_params.add_widget(p_card)

        # Guide Card
        g_card = BoxLayout(orientation="vertical", spacing=8, padding=16, size_hint_y=None, height=180)
        with g_card.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_SURFACE))
            g_card.bg = RoundedRectangle(pos=g_card.pos, size=g_card.size, radius=[6, 6, 6, 6])
            Color(*get_color_from_hex(Settings.COLOR_BORDER))
            g_card.line = Line(rounded_rectangle=[g_card.x, g_card.y, g_card.width, g_card.height, 6], width=1)

        g_card.bind(pos=_upd_cs, size=_upd_cs)

        g_title = Label(
            text="Free Cloud MySQL Hosting Guide",
            bold=True,
            font_size="13sp",
            color=get_color_from_hex(Settings.COLOR_PRIMARY),
            size_hint_y=None,
            height=20,
            halign="left",
        )
        g_title.bind(size=g_title.setter("text_size"))
        g_card.add_widget(g_title)

        guide_txt = (
            "1. Create a free MySQL database on Aiven.io, Clever Cloud, or PlanetScale.\n"
            "2. Import database/schema.sql and database/seed.sql.\n"
            "3. Copy .env.example to .env and input your host, user, and password.\n"
            "4. Click 'Test Connection & Reconnect' above to sync immediately."
        )
        g_lbl = Label(
            text=guide_txt,
            font_size="11sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_y=None,
            height=90,
            halign="left",
            valign="top",
        )
        g_lbl.bind(size=g_lbl.setter("text_size"))
        g_card.add_widget(g_lbl)

        grid_params.add_widget(g_card)
        box.add_widget(grid_params)

        # System Logging Information
        log_box = BoxLayout(orientation="vertical", spacing=6, padding=16, size_hint_y=None, height=90)
        with log_box.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_SURFACE))
            log_box.bg = RoundedRectangle(pos=log_box.pos, size=log_box.size, radius=[6, 6, 6, 6])
            Color(*get_color_from_hex(Settings.COLOR_BORDER))
            log_box.line = Line(rounded_rectangle=[log_box.x, log_box.y, log_box.width, log_box.height, 6], width=1)

        log_box.bind(pos=_upd_cs, size=_upd_cs)

        log_title = Label(
            text="Application Logging Location",
            bold=True,
            font_size="13sp",
            color=get_color_from_hex(Settings.COLOR_PRIMARY),
            size_hint_y=None,
            height=20,
            halign="left",
        )
        log_title.bind(size=log_title.setter("text_size"))
        log_box.add_widget(log_title)

        log_path_lbl = Label(
            text=f"Rotated system diagnostic logs written to:\n{LOG_FILE}",
            font_size="11sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_y=None,
            height=36,
            halign="left",
            valign="top",
        )
        log_path_lbl.bind(size=log_path_lbl.setter("text_size"))
        log_box.add_widget(log_path_lbl)
        box.add_widget(log_box)

        scroll.add_widget(box)
        root.add_widget(scroll)
        self.add_widget(root)

    def _make_kv(self, key: str, val: str) -> BoxLayout:
        row = BoxLayout(orientation="horizontal", size_hint_y=None, height=22)
        k_l = Label(
            text=f"{key}:",
            font_size="11sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_x=None,
            width=170,
            halign="left",
            valign="middle",
        )
        k_l.bind(size=k_l.setter("text_size"))
        row.add_widget(k_l)

        v_l = Label(
            text=val,
            bold=True,
            font_size="11sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_x=1,
            halign="left",
            valign="middle",
        )
        v_l.bind(size=v_l.setter("text_size"))
        row.add_widget(v_l)
        return row

    def on_enter(self) -> None:
        """Refreshes status when entering screen."""
        self.update_status_display()

    def update_status_display(self) -> None:
        """Updates diagnostic banner based on connection state."""
        if self.db.is_connected():
            self.lbl_status_badge.text = "● CONNECTED TO CLOUD MYSQL SERVER"
            self.lbl_status_badge.color = get_color_from_hex(Settings.COLOR_SUCCESS)
            self.lbl_status_detail.text = (
                f"Connected to remote database '{Settings.DB_NAME}' at {Settings.DB_HOST}:{Settings.DB_PORT}.\n"
                "All transaction commits, queries, and student records are synced live to MySQL."
            )
        else:
            self.lbl_status_badge.text = "● LOCAL DEMONSTRATION & EVALUATION MODE"
            self.lbl_status_badge.color = get_color_from_hex(Settings.COLOR_WARNING)
            self.lbl_status_detail.text = (
                "Operating in safe local mode with prepopulated test records. "
                "To link to a live online MySQL database, populate .env with your credentials and click Reconnect."
            )

    def test_reconnect(self) -> None:
        """Executes connection handshake test."""
        ok, msg = self.db.connect()
        self.update_status_display()
        InfoDialog("Connection Diagnostic", msg, is_error=(not ok)).open()
