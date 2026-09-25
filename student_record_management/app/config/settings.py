"""
Application settings and environment configuration.
Loads credentials safely from .env and configures application-wide logging.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOGS_DIR / "app.log"

# Load environment variables from .env
ENV_FILE = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_FILE)


class Settings:
    """Central configuration class for database and application behavior."""

    # Application metadata
    APP_NAME: str = "Student Record Management System"
    APP_VERSION: str = "1.0.0"
    ORGANIZATION: str = "Academic Administration"

    # Database parameters
    DB_HOST: str = os.getenv("DB_HOST", "").strip()
    DB_PORT: int = int(os.getenv("DB_PORT", "3306").strip() or 3306)
    DB_NAME: str = os.getenv("DB_NAME", "").strip()
    DB_USER: str = os.getenv("DB_USER", "").strip()
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "").strip()
    DB_POOL_NAME: str = os.getenv("DB_POOL_NAME", "student_pool").strip()
    DB_POOL_SIZE: int = int(os.getenv("DB_POOL_SIZE", "5").strip() or 5)
    DB_CONNECT_TIMEOUT: int = int(os.getenv("DB_CONNECT_TIMEOUT", "10").strip() or 10)

    # UI Theme Palette (Clean, human-designed institutional feel: Navy primary + Teal accent)
    COLOR_PRIMARY: str = "#1E3A8A"       # Deep Institutional Navy Blue
    COLOR_PRIMARY_DARK: str = "#172554"  # Very Dark Navy
    COLOR_PRIMARY_LIGHT: str = "#3B82F6" # Royal Blue accent
    COLOR_SECONDARY: str = "#0D9488"     # Teal accent
    COLOR_BACKGROUND: str = "#F8FAFC"    # Soft Light Neutral Slate
    COLOR_SURFACE: str = "#FFFFFF"       # Pure White for cards/forms
    COLOR_BORDER: str = "#E2E8F0"        # Subtle slate border
    COLOR_TEXT_PRIMARY: str = "#0F172A"  # Dark Slate
    COLOR_TEXT_SECONDARY: str = "#64748B"# Muted Gray Slate
    COLOR_SUCCESS: str = "#16A34A"       # Forest Green
    COLOR_WARNING: str = "#D97706"       # Amber
    COLOR_ERROR: str = "#DC2626"         # Crimson Red

    @classmethod
    def is_db_configured(cls) -> bool:
        """Checks if minimum database credentials have been specified."""
        return bool(cls.DB_HOST and cls.DB_NAME and cls.DB_USER)

    @classmethod
    def reload_env(cls) -> None:
        """Reloads .env variables in case they were updated at runtime."""
        load_dotenv(dotenv_path=ENV_FILE, override=True)
        cls.DB_HOST = os.getenv("DB_HOST", "").strip()
        cls.DB_PORT = int(os.getenv("DB_PORT", "3306").strip() or 3306)
        cls.DB_NAME = os.getenv("DB_NAME", "").strip()
        cls.DB_USER = os.getenv("DB_USER", "").strip()
        cls.DB_PASSWORD = os.getenv("DB_PASSWORD", "").strip()


def setup_logging() -> logging.Logger:
    """
    Configures rotating file logging and console logging.
    Never prints or logs database passwords.
    """
    logger = logging.getLogger("student_records")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s.%(module)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File handler (max 5MB, keep 3 backups)
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        # Console handler for debugging in VS Code terminal
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = setup_logging()


def get_settings() -> type[Settings]:
    """Retrieves the Settings class."""
    return Settings
