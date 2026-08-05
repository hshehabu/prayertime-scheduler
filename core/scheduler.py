import platform
import os
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker


class PrayerScheduler(QThread):
    """Background thread that manages countdowns and executes system actions."""

    # Signals
    countdown_tick = Signal(int, str, str)   # seconds_remaining, prayer_name, action_name
    action_imminent = Signal(str, str)       # prayer_name, action_name
    action_triggered = Signal(str, str)      # prayer_name, action_name
    no_upcoming_prayer = Signal()
    prayer_schedule_updated = Signal(str, int)  # next_prayer_name, seconds_to_action

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.prayer_times: Dict[str, datetime] = {}
        self.running = False
        self.paused = False

        self.next_prayer_name: Optional[str] = None
        self.next_prayer_time: Optional[datetime] = None
        self.next_action_time: Optional[datetime] = None
        self.next_action_name: Optional[str] = None

        self.snoozing = False
        self.snooze_until: Optional[datetime] = None
        self.skip_next = False
        self._imminent_emitted = False

        self.mutex = QMutex()

    def update_prayer_times(self, times: Dict[str, datetime]):
        """Update schedule with new prayer times."""
        with QMutexLocker(self.mutex):
            self.prayer_times = times
            self._calculate_next_event()

    def _get_action_for_prayer(self, prayer_name: str) -> str:
        per_prayer = self.config.get("per_prayer_actions") or {}
        return per_prayer.get(prayer_name, self.config.get("default_action"))

    def _calculate_next_event(self):
        """Determine the next prayer and when to alert/act."""
        if not self.prayer_times:
            return

        now = datetime.now()
        lead_minutes = self.config.get("alert_minutes_before")

        # Reset all next-event state
        self.next_prayer_name = None
        self.next_prayer_time = None
        self.next_action_time = None
        self.next_action_name = None
        self._imminent_emitted = False

        # Find the earliest upcoming prayer whose action time is still in the future
        for prayer, p_time in self.prayer_times.items():
            action_time = p_time - timedelta(minutes=lead_minutes)
            if action_time > now:
                if self.next_action_time is None or action_time < self.next_action_time:
                    self.next_action_time = action_time
                    self.next_prayer_time = p_time
                    self.next_prayer_name = prayer
                    self.next_action_name = self._get_action_for_prayer(prayer)

        if self.next_prayer_name:
            secs = int((self.next_action_time - now).total_seconds())
            self.prayer_schedule_updated.emit(self.next_prayer_name, secs)
            logging.info(f"Next event: {self.next_action_name} for {self.next_prayer_name} in {secs}s")
        else:
            self.no_upcoming_prayer.emit()
            logging.info("No upcoming prayers for today.")

    def toggle_pause(self, paused: bool):
        with QMutexLocker(self.mutex):
            self.paused = paused

    def skip_next_prayer(self):
        with QMutexLocker(self.mutex):
            self.skip_next = True
            self.snoozing = False
            self._imminent_emitted = False

    def snooze(self):
        with QMutexLocker(self.mutex):
            snooze_mins = self.config.get("snooze_minutes")
            self.snooze_until = datetime.now() + timedelta(minutes=snooze_mins)
            self.snoozing = True

    def execute_now(self):
        with QMutexLocker(self.mutex):
            action = self.next_action_name or self.config.get("default_action")
            prayer = self.next_prayer_name or "Manual"
            self.snoozing = False
            self._execute_system_action(action, prayer)
            self.skip_next = True

    def run(self):
        self.running = True
        while self.running:
            time.sleep(1)

            with QMutexLocker(self.mutex):
                if self.paused or not self.next_prayer_name:
                    continue

                now = datetime.now()

                if self.skip_next:
                    if self.next_prayer_time and now > self.next_prayer_time:
                        self.skip_next = False
                        self._calculate_next_event()
                    continue

                # Snooze countdown
                if self.snoozing and self.snooze_until:
                    secs_left = int((self.snooze_until - now).total_seconds())
                    if secs_left <= 0:
                        self.snoozing = False
                        self._execute_system_action(self.next_action_name, self.next_prayer_name)
                        self.skip_next = True
                    else:
                        self.countdown_tick.emit(secs_left, f"{self.next_prayer_name} (Snoozed)", self.next_action_name)
                    continue

                # Normal countdown to action time
                secs_to_action = int((self.next_action_time - now).total_seconds())

                if secs_to_action > 0:
                    self.countdown_tick.emit(secs_to_action, self.next_prayer_name, self.next_action_name)
                else:
                    # Action time reached
                    if not self._imminent_emitted:
                        self._imminent_emitted = True
                        if self.config.get("snooze_enabled"):
                            self.action_imminent.emit(self.next_prayer_name, self.next_action_name)
                            self.snoozing = True
                            self.snooze_until = now + timedelta(minutes=self.config.get("snooze_minutes"))
                        else:
                            self._execute_system_action(self.next_action_name, self.next_prayer_name)
                            self.skip_next = True

    def _execute_system_action(self, action: str, prayer: str):
        """Execute the OS level command."""
        self.action_triggered.emit(prayer, action)
        logging.info(f"Executing action '{action}' for {prayer}")

        if action == "notification":
            return  # The UI handles the notification via the signal

        try:
            current_os = platform.system()
            if current_os == "Windows":
                if action == "sleep":
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                elif action == "hibernate":
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 1,1,0")
                elif action == "shutdown":
                    os.system("shutdown /s /t 0")
                elif action == "lock":
                    os.system("rundll32.exe user32.dll,LockWorkStation")
        except Exception as e:
            logging.error(f"Failed to execute {action}: {e}")

    def stop(self):
        self.running = False
        self.wait()
