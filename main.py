"""
PrayerTime Scheduler — Modern Windows Desktop Application
Entry point: initializes config, API, scheduler, UI, and system tray.
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from core.config import AppConfig
from core.api import PrayerTimeAPI
from core.scheduler import PrayerScheduler
from ui.tray import SystemTrayManager
from ui.main_window import MainWindow


def get_icon_path() -> str:
    """Resolve icon path for both dev and PyInstaller bundle."""
    if getattr(sys, '_MEIPASS', None):
        return os.path.join(sys._MEIPASS, "assets", "icon.png")
    return os.path.join(os.path.dirname(__file__), "assets", "icon.png")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PrayerTime Scheduler")
    app.setQuitOnLastWindowClosed(False)  # Keep running after window close (tray)

    icon_path = get_icon_path()
    app.setWindowIcon(QIcon(icon_path))

    # Core
    config = AppConfig()
    api = PrayerTimeAPI(config)
    scheduler = PrayerScheduler(config)

    # UI
    tray = SystemTrayManager(icon_path)
    tray.show()

    window = MainWindow(config, api, scheduler, tray, icon_path)

    if config.get("start_minimized"):
        tray.show_toast("PrayerTime Scheduler", "Running in the background.")
    else:
        window.show()

    # Start scheduler thread
    scheduler.start()

    exit_code = app.exec()
    scheduler.stop()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
