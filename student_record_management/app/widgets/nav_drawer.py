"""
Navigation drawer and header bar widget.
Provides adaptive navigation supporting desktop sidebar and responsive mobile layout.
"""

from typing import Callable, Dict
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

from app.config.settings import Settings


NAV_ITEMS = [
    ("dashboard", "Dashboard"),
    ("students", "Students"),
    ("attendance", "Attendance"),
    ("marks", "Marks & Grades"),
    ("departments", "Departments"),
    ("reports", "Reports"),
    ("settings", "Database / Settings"),
]


class SidebarNavigation(BoxLayout):
    """
    Primary application navigation sidebar.
    Highlights current active section and adapts width automatically.
    """

    def __init__(self, switch_screen_callback: Callable[[str], None], **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_x = None
        self.width = 220
        self.padding = [12, 16, 12, 16]
        self.spacing = 8
        self.switch_screen = switch_screen_callback
        self.active_screen_name = "dashboard"
        self.buttons: Dict[str, Button] = {}

        # Sidebar background
        with self.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_PRIMARY_DARK))
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            Color(*get_color_from_hex("#1E293B"))
            self.border_line = Line(points=[self.x + self.width, self.y, self.x + self.width, self.y + self.height], width=1)

        self.bind(pos=self._update_bg, size=self._update_bg)

        # Institution Brand Header
        brand_box = BoxLayout(orientation="vertical", size_hint_y=None, height=65, spacing=4)
        brand_title = Label(
            text="ScholarPulse",
            font_size="16sp",
            bold=True,
            color=get_color_from_hex("#FFFFFF"),
            size_hint_y=None,
            height=26,
            halign="left",
            valign="middle",
        )
        brand_title.bind(size=brand_title.setter("text_size"))
        brand_box.add_widget(brand_title)

        brand_sub = Label(
            text="Academic Records & Intelligence",
            font_size="10.5sp",
            color=get_color_from_hex("#94A3B8"),
            size_hint_y=None,
            height=20,
            halign="left",
            valign="middle",
        )
        brand_sub.bind(size=brand_sub.setter("text_size"))
        brand_box.add_widget(brand_sub)
        self.add_widget(brand_box)

        # Nav items
        for key, label in NAV_ITEMS:
            btn = Button(
                text=f"  {label}",
                font_size="13sp",
                size_hint_y=None,
                height=42,
                halign="left",
                valign="middle",
            )
            btn.bind(size=btn.setter("text_size"))
            btn.bind(on_release=lambda instance, k=key: self._on_item_click(k))
            self.buttons[key] = btn
            self.add_widget(btn)

        # Spacer
        self.add_widget(BoxLayout(size_hint_y=1))

        # Exit / Close App button at bottom
        btn_exit = Button(
            text="  Exit Application",
            font_size="12sp",
            size_hint_y=None,
            height=38,
            halign="left",
            valign="middle",
            background_color=get_color_from_hex("#334155"),
            color=get_color_from_hex("#F87171"),
        )
        btn_exit.bind(size=btn_exit.setter("text_size"))
        btn_exit.bind(on_release=lambda x: self._on_item_click("exit"))
        self.add_widget(btn_exit)

        self.set_active("dashboard")

    def _update_bg(self, *args) -> None:
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.points = [self.x + self.width, self.y, self.x + self.width, self.y + self.height]

    def _on_item_click(self, key: str) -> None:
        self.set_active(key)
        self.switch_screen(key)

    def set_active(self, key: str) -> None:
        """Updates visual button styling for current active page."""
        self.active_screen_name = key
        for k, btn in self.buttons.items():
            if k == key:
                btn.background_color = get_color_from_hex(Settings.COLOR_PRIMARY_LIGHT)
                btn.color = get_color_from_hex("#FFFFFF")
                btn.bold = True
            else:
                btn.background_color = get_color_from_hex(Settings.COLOR_PRIMARY_DARK)
                btn.color = get_color_from_hex("#CBD5E1")
                btn.bold = False


class AppHeaderBar(BoxLayout):
    """
    Standard top header bar showing page title, current user status, and mobile drawer toggle.
    """

    def __init__(self, title: str, on_toggle_menu: Optional[Callable[[], None]] = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = 54
        self.padding = [16, 8, 16, 8]
        self.spacing = 10

        with self.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_SURFACE))
            self.bg = Rectangle(pos=self.pos, size=self.size)
            Color(*get_color_from_hex(Settings.COLOR_BORDER))
            self.border = Line(points=[self.x, self.y, self.x + self.width, self.y], width=1)

        self.bind(pos=self._update_bar, size=self._update_bar)

        # Mobile toggle button
        if on_toggle_menu:
            btn_menu = Button(
                text="☰",
                font_size="18sp",
                size_hint=(None, None),
                size=(36, 36),
                background_color=get_color_from_hex(Settings.COLOR_PRIMARY),
                color=get_color_from_hex("#FFFFFF"),
            )
            btn_menu.bind(on_release=lambda x: on_toggle_menu())
            self.add_widget(btn_menu)

        # Page Title
        self.lbl_title = Label(
            text=title,
            bold=True,
            font_size="17sp",
            color=get_color_from_hex(Settings.COLOR_PRIMARY_DARK),
            size_hint_x=1,
            halign="left",
            valign="middle",
        )
        self.lbl_title.bind(size=self.lbl_title.setter("text_size"))
        self.add_widget(self.lbl_title)

    def _update_bar(self, *args) -> None:
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.border.points = [self.x, self.y, self.x + self.width, self.y]

    def set_title(self, new_title: str) -> None:
        self.lbl_title.text = new_title
