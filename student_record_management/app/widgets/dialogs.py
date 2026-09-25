"""
Modal dialog components for confirmations, alerts, and notifications.
"""

from typing import Callable, Optional
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex

from app.config.settings import Settings


class ConfirmDialog(Popup):
    """
    Modal confirmation dialog for destructive or critical actions (e.g. Delete Student).
    """

    def __init__(
        self,
        title: str,
        message: str,
        on_confirm: Callable[[], None],
        on_cancel: Optional[Callable[[], None]] = None,
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
        destructive: bool = True,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (None, None)
        self.size = (420, 210)
        self.auto_dismiss = False

        content = BoxLayout(orientation="vertical", padding=16, spacing=14)

        # Message body
        lbl = Label(
            text=message,
            font_size="13sp",
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            halign="center",
            valign="middle",
        )
        lbl.bind(size=lbl.setter("text_size"))
        content.add_widget(lbl)

        # Button row
        btn_box = BoxLayout(orientation="horizontal", spacing=12, size_hint_y=None, height=38)

        # Cancel Button
        btn_cancel = Button(
            text=cancel_text,
            background_color=get_color_from_hex(Settings.COLOR_BORDER),
            color=get_color_from_hex(Settings.COLOR_TEXT_PRIMARY),
            bold=True,
        )

        def _do_cancel(*args):
            self.dismiss()
            if on_cancel:
                on_cancel()

        btn_cancel.bind(on_release=_do_cancel)
        btn_box.add_widget(btn_cancel)

        # Confirm Button
        btn_confirm_color = Settings.COLOR_ERROR if destructive else Settings.COLOR_PRIMARY
        btn_confirm = Button(
            text=confirm_text,
            background_color=get_color_from_hex(btn_confirm_color),
            color=get_color_from_hex("#FFFFFF"),
            bold=True,
        )

        def _do_confirm(*args):
            self.dismiss()
            on_confirm()

        btn_confirm.bind(on_release=_do_confirm)
        btn_box.add_widget(btn_confirm)

        content.add_widget(btn_box)
        self.content = content


class InfoDialog(Popup):
    """
    Standard modal for displaying operational success, warnings, or error messages.
    """

    def __init__(
        self,
        title: str,
        message: str,
        is_error: bool = False,
        on_close: Optional[Callable[[], None]] = None,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.title = title
        self.size_hint = (None, None)
        self.size = (400, 200)

        content = BoxLayout(orientation="vertical", padding=16, spacing=14)

        msg_color = Settings.COLOR_ERROR if is_error else Settings.COLOR_TEXT_PRIMARY
        lbl = Label(
            text=message,
            font_size="13sp",
            color=get_color_from_hex(msg_color),
            halign="center",
            valign="middle",
        )
        lbl.bind(size=lbl.setter("text_size"))
        content.add_widget(lbl)

        btn_ok = Button(
            text="OK",
            size_hint_y=None,
            height=36,
            background_color=get_color_from_hex(Settings.COLOR_PRIMARY),
            color=get_color_from_hex("#FFFFFF"),
            bold=True,
        )

        def _dismiss_and_call(*args):
            self.dismiss()
            if on_close:
                on_close()

        btn_ok.bind(on_release=_dismiss_and_call)
        content.add_widget(btn_ok)

        self.content = content
