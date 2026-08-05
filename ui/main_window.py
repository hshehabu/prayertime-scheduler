import os
from PySide6.QtWidgets import QMainWindow, QTabWidget, QMessageBox, QApplication
from PySide6.QtGui import QIcon, QCloseEvent
from PySide6.QtCore import Qt

from .dashboard import Dashboard
from .settings_panel import SettingsPanel
from .snooze_dialog import SnoozeDialog
from .floating_widget import FloatingWidget
from .theme import ThemeManager


class MainWindow(QMainWindow):
    def __init__(self, config, api, scheduler, tray, app_icon_path):
        super().__init__()
        self.config = config
        self.api = api
        self.scheduler = scheduler
        self.tray = tray

        self.setWindowTitle("🕌 PrayerTime Scheduler")
        self.setWindowIcon(QIcon(app_icon_path))
        self.resize(850, 580)

        # ── Tab Widget ──
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.dashboard = Dashboard(self.config)
        self.settings = SettingsPanel(self.config)

        self.tabs.addTab(self.dashboard, "🕌  Dashboard")
        self.tabs.addTab(self.settings, "⚙  Settings")

        # ── Floating Widget ──
        self.floating = FloatingWidget()
        self.floating.show_main_requested.connect(self.showNormal)
        self.floating.show_main_requested.connect(self.activateWindow)
        self.floating.show()

        self.snooze_dialog = None

        self._connect_signals()

        # Apply theme
        ThemeManager.apply_theme(self.config.get("theme"))

        # Fetch prayer times
        self.api.fetch_times_async()

    def _connect_signals(self):
        # API
        self.api.times_fetched.connect(self.on_times_fetched)
        self.api.fetch_failed.connect(self.on_fetch_failed)
        self.api.location_detected.connect(self.on_location_detected)

        # Scheduler
        self.scheduler.countdown_tick.connect(self.on_countdown_tick)
        self.scheduler.action_imminent.connect(self.on_action_imminent)
        self.scheduler.action_triggered.connect(self.on_action_triggered)
        self.scheduler.no_upcoming_prayer.connect(self.on_no_upcoming)

        # Dashboard
        self.dashboard.pause_toggled.connect(self.on_pause_toggled)
        self.dashboard.skip_requested.connect(self.scheduler.skip_next_prayer)
        self.dashboard.trigger_now_requested.connect(self.scheduler.execute_now)

        # Settings
        self.settings.settings_changed.connect(self.on_settings_changed)
        self.settings.location_detect_requested.connect(self.api.auto_detect_location_async)

        # Tray
        self.tray.show_requested.connect(self.showNormal)
        self.tray.show_requested.connect(self.activateWindow)
        self.tray.exit_requested.connect(self.force_close)
        self.tray.pause_toggled.connect(self._sync_pause_from_tray)

    # ── Slots ──

    def on_times_fetched(self, times):
        self.dashboard.update_prayer_times(times)
        self.scheduler.update_prayer_times(times)

    def on_fetch_failed(self, err_msg):
        self.tray.show_toast("Fetch Failed", err_msg)

    def on_location_detected(self, city, country):
        self.settings.set_location(city, country)
        self.tray.show_toast("Location Detected", f"{city}, {country}")

    def on_countdown_tick(self, secs_left, prayer_name, action_name):
        self.dashboard.update_countdown(secs_left, prayer_name, action_name)
        self.floating.update_countdown(secs_left, prayer_name, action_name)

        # Update tray every 30 seconds
        if secs_left % 30 == 0:
            mins = secs_left // 60
            status = f"Next: {action_name.title()} in {mins}m for {prayer_name}"
            self.tray.update_tooltip(status)
            self.tray.update_status(status)

    def on_no_upcoming(self):
        self.dashboard.set_no_upcoming()
        self.floating.set_no_upcoming()
        self.tray.update_status("All prayers done for today")
        self.tray.update_tooltip("PrayerTime Scheduler — All prayers done")

    def on_action_imminent(self, prayer_name, action_name):
        self.tray.show_toast(
            "🕌 Action Imminent",
            f"PC will {action_name} for {prayer_name} prayer. Click tray to manage.",
        )

        if self.snooze_dialog:
            self.snooze_dialog.close()

        timeout = self.config.get("snooze_minutes") * 60
        self.snooze_dialog = SnoozeDialog(prayer_name, action_name, timeout_secs=timeout, parent=self)
        self.snooze_dialog.snooze_requested.connect(self.scheduler.snooze)
        self.snooze_dialog.execute_now_requested.connect(self.scheduler.execute_now)
        self.snooze_dialog.cancel_requested.connect(self.scheduler.skip_next_prayer)
        self.snooze_dialog.show()

    def on_action_triggered(self, prayer_name, action_name):
        self.tray.show_toast("Action Executed", f"Triggered {action_name} for {prayer_name}.")

    def on_pause_toggled(self, is_paused):
        self.scheduler.toggle_pause(is_paused)
        self.tray.set_paused_state(is_paused)
        if is_paused:
            self.tray.update_tooltip("PrayerTime Scheduler (Paused)")
            self.tray.update_status("Status: Paused")
            self.floating.set_paused()

    def _sync_pause_from_tray(self, is_paused):
        self.dashboard.btn_pause.setChecked(is_paused)
        self.dashboard._on_pause_clicked()

    def on_settings_changed(self):
        ThemeManager.apply_theme(self.config.get("theme"))
        self.dashboard.location_label.setText(
            f"📍 {self.config.get('city')}, {self.config.get('country')}"
        )
        self.api.fetch_times_async()

    def closeEvent(self, event: QCloseEvent):
        event.ignore()
        self.hide()
        self.tray.show_toast("Minimized", "PrayerTime Scheduler is still running in the background.")

    def force_close(self):
        self.floating.close()
        self.scheduler.stop()
        QApplication.quit()
