"""
PrayerTime Scheduler — Modern Windows Desktop Application
Entry point with single-instance enforcement.
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSharedMemory

from core.config import AppConfig
from core.api import PrayerTimeAPI
from core.scheduler import PrayerScheduler
from ui.tray import SystemTrayManager
from ui.main_window import MainWindow


_INSTANCE_KEY = "PrayerTimeScheduler_SingleInstance_KesbTech"


def get_icon_path() -> str:
    """Resolve icon path for both dev and PyInstaller bundle."""
    if getattr(sys, "_MEIPASS", None):
        return os.path.join(sys._MEIPASS, "assets", "icon.png")
    return os.path.join(os.path.dirname(__file__), "assets", "icon.png")


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PrayerTime Scheduler")
    app.setOrganizationName("Kesb Tech")
    app.setQuitOnLastWindowClosed(False)

    # ── Single-instance guard ──
    shared = QSharedMemory(_INSTANCE_KEY)
    if not shared.create(1):
        # Another instance is already running — try to bring it forward
        import ctypes
        user32 = ctypes.windll.user32
        hwnd = user32.FindWindowW(None, "🕌 PrayerTime Scheduler")
        if hwnd:
            SW_RESTORE = 9
            user32.ShowWindow(hwnd, SW_RESTORE)
            user32.SetForegroundWindow(hwnd)
        sys.exit(0)

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

    scheduler.start()

    exit_code = app.exec()
    scheduler.stop()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
