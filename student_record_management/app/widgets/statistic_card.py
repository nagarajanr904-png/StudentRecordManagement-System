"""
Metric card widget for administrative dashboard summaries.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex

from app.config.settings import Settings


class StatisticCard(BoxLayout):
    """
    Standard institutional summary card:
    Displays numeric metrics with subtle borders, clean background, and clear typography.
    """

    def __init__(
        self,
        title: str,
        value: str,
        subtitle: str = "",
        accent_color: str = Settings.COLOR_PRIMARY,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [18, 16, 18, 16]
        self.spacing = 4
        self.size_hint_y = None
        self.height = 110
        self.accent_hex = accent_color

        # Background drawing with subtle border
        with self.canvas.before:
            Color(*get_color_from_hex(Settings.COLOR_SURFACE))
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[6, 6, 6, 6])
            Color(*get_color_from_hex(Settings.COLOR_BORDER))
            self.border_line = Line(rounded_rectangle=[self.x, self.y, self.width, self.height, 6], width=1)
            # Top accent stripe
            Color(*get_color_from_hex(self.accent_hex))
            self.top_stripe = RoundedRectangle(pos=[self.x, self.y + self.height - 4], size=[self.width, 4], radius=[6, 6, 0, 0])

        self.bind(pos=self._update_rects, size=self._update_rects)

        # Title
        self.lbl_title = Label(
            text=title.upper(),
            font_size="12sp",
            bold=True,
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_y=None,
            height=18,
            halign="left",
            valign="middle",
        )
        self.lbl_title.bind(size=self.lbl_title.setter("text_size"))
        self.add_widget(self.lbl_title)

        # Main numeric value
        self.lbl_val = Label(
            text=value,
            font_size="28sp",
            bold=True,
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            size_hint_y=None,
            height=40,
            halign="left",
            valign="middle",
        )
        self.lbl_val.bind(size=self.lbl_val.setter("text_size"))
        self.add_widget(self.lbl_val)

        # Subtitle
        self.lbl_sub = Label(
            text=subtitle,
            font_size="11sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_SECONDARY),
            size_hint_y=None,
            height=18,
            halign="left",
            valign="middle",
        )
        self.lbl_sub.bind(size=self.lbl_sub.setter("text_size"))
        self.add_widget(self.lbl_sub)

    def _update_rects(self, *args) -> None:
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_line.rounded_rectangle = [self.x, self.y, self.width, self.height, 6]
        self.top_stripe.pos = [self.x, self.y + self.height - 4]
        self.top_stripe.size = [self.width, 4]

    def update_value(self, new_val: str, subtitle: str = "") -> None:
        """Updates metric value dynamically."""
        self.lbl_val.text = str(new_val)
        if subtitle:
            self.lbl_sub.text = subtitle
