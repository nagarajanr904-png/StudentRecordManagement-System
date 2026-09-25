#!/usr/bin/env python3
"""
Student Record Management System
==============================================================================
Production-style institutional desktop & mobile administrative system
built with Python, MySQL, and Kivy.

Author: Senior Python Software Architect
License: Educational & Academic Enterprise
==============================================================================
"""

import sys
import os
from pathlib import Path

# Add current project root to python path for clean package imports
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Kivy configuration before other Kivy imports
from kivy.config import Config
Config.set('graphics', 'width', '1180')
Config.set('graphics', 'height', '740')
Config.set('graphics', 'minimum_width', '600')
Config.set('graphics', 'minimum_height', '480')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition, NoTransition
from kivy.utils import get_color_from_hex

from app.config.settings import Settings, logger
from app.database.connection import get_db
from app.widgets.nav_drawer import SidebarNavigation, AppHeaderBar
from app.widgets.dialogs import ConfirmDialog
from app.screens.dashboard import DashboardScreen
from app.screens.students import StudentsScreen
from app.screens.student_form import StudentFormScreen
from app.screens.student_details import StudentDetailsScreen
from app.screens.attendance import AttendanceScreen
from app.screens.marks import MarksScreen
from app.screens.departments import DepartmentsScreen
from app.screens.reports import ReportsScreen
from app.screens.settings_screen import SettingsScreen


class StudentRecordApp(App):
    """
    Main Kivy Application coordinating the Window, Navigation Sidebar,
    ScreenManager, and Database lifecycle.
    """

    title = "Student Record Management System"

    def build(self):
        # Set clear window background color
        Window.clearcolor = get_color_from_hex(Settings.COLOR_BACKGROUND)
        Window.bind(on_resize=self._on_window_resize)

        # Initialize Database connection
        self.db = get_db()
        if not self.db.is_connected():
            logger.info("Starting in offline demonstration mode. To connect to MySQL, configure .env.")

        # Root layout (Horizontal: Sidebar Navigation + Main Screen Content Area)
        self.root_layout = BoxLayout(orientation="horizontal")

        # Sidebar navigation
        self.sidebar = SidebarNavigation(switch_screen_callback=self.handle_navigation)
        self.root_layout.add_widget(self.sidebar)

        # Right-side content container (Header Bar + ScreenManager)
        self.content_area = BoxLayout(orientation="vertical")

        # Top Header Bar
        self.header_bar = AppHeaderBar(
            title="Dashboard",
            on_toggle_menu=self.toggle_sidebar_mobile
        )
        self.content_area.add_widget(self.header_bar)

        # Screen Manager
        self.sm = ScreenManager(transition=NoTransition())

        # Register all application screens
        self.dashboard_screen = DashboardScreen(name="dashboard", switch_screen_cb=self.handle_navigation)
        self.students_screen = StudentsScreen(name="students", switch_screen_cb=self.handle_navigation)
        self.student_form_screen = StudentFormScreen(name="student_form", switch_screen_cb=self.handle_navigation)
        self.student_details_screen = StudentDetailsScreen(name="student_details", switch_screen_cb=self.handle_navigation)
        self.attendance_screen = AttendanceScreen(name="attendance", switch_screen_cb=self.handle_navigation)
        self.marks_screen = MarksScreen(name="marks", switch_screen_cb=self.handle_navigation)
        self.departments_screen = DepartmentsScreen(name="departments", switch_screen_cb=self.handle_navigation)
        self.reports_screen = ReportsScreen(name="reports", switch_screen_cb=self.handle_navigation)
        self.settings_screen = SettingsScreen(name="settings", switch_screen_cb=self.handle_navigation)

        self.sm.add_widget(self.dashboard_screen)
        self.sm.add_widget(self.students_screen)
        self.sm.add_widget(self.student_form_screen)
        self.sm.add_widget(self.student_details_screen)
        self.sm.add_widget(self.attendance_screen)
        self.sm.add_widget(self.marks_screen)
        self.sm.add_widget(self.departments_screen)
        self.sm.add_widget(self.reports_screen)
        self.sm.add_widget(self.settings_screen)

        self.content_area.add_widget(self.sm)
        self.root_layout.add_widget(self.content_area)

        # Check screen width initially for responsive sizing
        self._on_window_resize(Window, Window.width, Window.height)

        logger.info("Application interface initialized successfully.")
        return self.root_layout

    def handle_navigation(self, screen_name: str, payload: any = None) -> None:
        """
        Coordinates screen transitions and data passing between screens.
        """
        if screen_name == "exit":
            self.confirm_exit()
            return

        # Titles for header bar
        titles = {
            "dashboard": "Executive Dashboard",
            "students": "Student Registry Directory",
            "student_form": "Register New Student",
            "student_details": "Student Academic Dossier",
            "attendance": "Daily Attendance Audit",
            "marks": "Examination Marks & Results",
            "departments": "Academic Departments & Classes",
            "reports": "Reports & Data Export Center",
            "settings": "Database & Environment Diagnostics",
        }

        # Handle parameterized transitions
        if screen_name == "student_form":
            self.student_form_screen.set_editing_student(payload)
            if payload:
                self.header_bar.set_title("Edit Student Record")
            else:
                self.header_bar.set_title("Register New Student")
            self.sidebar.set_active("students")
            self.sm.current = "student_form"
            return

        if screen_name == "student_details":
            if payload:
                self.student_details_screen.load_student(payload)
            self.header_bar.set_title("Student Profile")
            self.sidebar.set_active("students")
            self.sm.current = "student_details"
            return

        # Standard navigation
        self.header_bar.set_title(titles.get(screen_name, "Student Records System"))
        self.sidebar.set_active(screen_name)
        self.sm.current = screen_name

        # On small screens, automatically collapse sidebar upon navigating
        if Window.width < 768 and self.sidebar.width > 0:
            self.sidebar.width = 0

    def toggle_sidebar_mobile(self) -> None:
        """Toggles sidebar visibility on narrow screens."""
        if self.sidebar.width == 0:
            self.sidebar.width = 220
        else:
            self.sidebar.width = 0

    def _on_window_resize(self, window, width, height) -> None:
        """
        Adaptive responsive layout adjustments:
        Automatically contracts sidebar into compact drawer on tablet/mobile screens.
        """
        if width < 768:
            # Mobile / narrow tablet
            self.sidebar.width = 0  # Collapsed by default, toggled via header hamburger button
        else:
            # Desktop / laptop
            self.sidebar.width = 220

    def confirm_exit(self) -> None:
        """Prompts confirmation before closing the application."""
        def do_stop():
            logger.info("User initiated application exit.")
            self.stop()

        ConfirmDialog(
            title="Exit Application",
            message="Are you sure you want to close the Student Record Management System?",
            confirm_text="Exit System",
            cancel_text="Stay",
            destructive=False,
            on_confirm=do_stop,
        ).open()


if __name__ == "__main__":
    app = StudentRecordApp()
    app.run()
