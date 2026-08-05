from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox,
)
from PySide6.QtCore import Qt, QTimer
from datetime import datetime
from .widgets import PrayerTimeCard, ActionButton


class Dashboard(QWidget):
    """Main dashboard view with hero header, prayer grid, and quick actions."""

    from PySide6.QtCore import Signal
    pause_toggled = Signal(bool)
    skip_requested = Signal()
    trigger_now_requested = Signal()

    PRAYER_ORDER = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self._prayer_datetimes = {}

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)

        # ── Islamic decorative header ──
        bismillah = QLabel("﷽")
        bismillah_font = bismillah.font()
        bismillah_font.setPointSize(20)
        bismillah.setFont(bismillah_font)
        bismillah.setAlignment(Qt.AlignCenter)
        bismillah.setStyleSheet("color: #D4A843; margin-bottom: 4px;")

        # ── Hero Header ──
        self.time_label = QLabel("--:-- --")
        self.time_label.setProperty("class", "HeroTime")
        time_font = self.time_label.font()
        time_font.setPointSize(42)
        time_font.setBold(True)
        self.time_label.setFont(time_font)
        self.time_label.setAlignment(Qt.AlignCenter)

        self.date_label = QLabel("")
        date_font = self.date_label.font()
        date_font.setPointSize(10)
        self.date_label.setFont(date_font)
        self.date_label.setAlignment(Qt.AlignCenter)
        self.date_label.setStyleSheet("color: #8B949E;")

        self.location_label = QLabel(f"📍 {self.config.get('city')}, {self.config.get('country')}")
        self.location_label.setProperty("class", "LocationLabel")
        loc_font = self.location_label.font()
        loc_font.setPointSize(11)
        self.location_label.setFont(loc_font)
        self.location_label.setAlignment(Qt.AlignCenter)

        self.countdown_label = QLabel("🕌  Waiting for prayer schedule...")
        self.countdown_label.setProperty("class", "HeroCountdown")
        cd_font = self.countdown_label.font()
        cd_font.setPointSize(14)
        cd_font.setBold(True)
        self.countdown_label.setFont(cd_font)
        self.countdown_label.setAlignment(Qt.AlignCenter)

        header = QVBoxLayout()
        header.setSpacing(4)
        header.addWidget(bismillah)
        header.addWidget(self.time_label)
        header.addWidget(self.date_label)
        header.addWidget(self.location_label)
        header.addSpacing(8)
        header.addWidget(self.countdown_label)

        # ── Prayer Grid ──
        grid = QHBoxLayout()
        grid.setSpacing(12)
        self.prayer_cards = {}
        for p in self.PRAYER_ORDER:
            card = PrayerTimeCard(p)
            self.prayer_cards[p] = card
            grid.addWidget(card)

        # ── Quick Actions ──
        actions = QHBoxLayout()
        actions.setSpacing(12)

        self.btn_pause = ActionButton("⏸  Pause Automation")
        self.btn_pause.setCheckable(True)
        self.btn_pause.clicked.connect(self._on_pause_clicked)

        self.btn_skip = ActionButton("⏭  Skip Next")
        self.btn_skip.clicked.connect(self._on_skip_clicked)

        self.btn_trigger = ActionButton("⚡  Trigger Now")
        self.btn_trigger.clicked.connect(self._on_trigger_clicked)

        actions.addStretch()
        actions.addWidget(self.btn_pause)
        actions.addWidget(self.btn_skip)
        actions.addWidget(self.btn_trigger)
        actions.addStretch()

        layout.addLayout(header)
        layout.addSpacing(8)
        layout.addLayout(grid)
        layout.addStretch()
        layout.addLayout(actions)

        # ── Clock timer ──
        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)
        self._update_clock()

    # ── Clock ──
    def _update_clock(self):
        now = datetime.now()
        self.time_label.setText(now.strftime("%I:%M:%S %p").lstrip("0"))
        self.date_label.setText(now.strftime("%A, %B %d, %Y"))

    # ── Data Updates ──
    def update_prayer_times(self, times):
        self._prayer_datetimes = times
        self._refresh_cards()

    def _refresh_cards(self):
        now = datetime.now()
        for prayer in self.PRAYER_ORDER:
            p_time = self._prayer_datetimes.get(prayer)
            if not p_time:
                continue
            time_str = p_time.strftime("%I:%M %p").lstrip("0")
            action = (self.config.get("per_prayer_actions") or {}).get(
                prayer, self.config.get("default_action")
            )
            is_passed = p_time < now
            status = f"{action.title()}" + (" · Passed" if is_passed else "")
            self.prayer_cards[prayer].update_data(
                time_str, status, is_active=False, is_passed=is_passed
            )

    def update_countdown(self, secs_left, prayer_name, action_name):
        hours = secs_left // 3600
        minutes = (secs_left % 3600) // 60
        seconds = secs_left % 60

        if hours > 0:
            time_str = f"{hours:02d}h {minutes:02d}m {seconds:02d}s"
        else:
            time_str = f"{minutes:02d}m {seconds:02d}s"

        lead = self.config.get("alert_minutes_before")
        self.countdown_label.setText(
            f"🕌  {action_name.title()} in {time_str}  ·  {lead}m before {prayer_name}"
        )

        # Highlight active card, dim passed ones
        now = datetime.now()
        for p in self.PRAYER_ORDER:
            p_time = self._prayer_datetimes.get(p)
            if not p_time:
                continue
            time_disp = p_time.strftime("%I:%M %p").lstrip("0")
            action = (self.config.get("per_prayer_actions") or {}).get(
                p, self.config.get("default_action")
            )
            is_passed = p_time < now
            is_active = prayer_name.startswith(p)
            status = f"{action.title()}"
            if is_passed:
                status += " · Passed"
            elif is_active:
                status += " · Next ▶"
            self.prayer_cards[p].update_data(time_disp, status, is_active=is_active, is_passed=is_passed)

    def set_no_upcoming(self):
        self.countdown_label.setText("🕌  All prayers have passed for today. See you tomorrow, In Shaa Allah!")
        now = datetime.now()
        for p in self.PRAYER_ORDER:
            p_time = self._prayer_datetimes.get(p)
            if p_time:
                time_disp = p_time.strftime("%I:%M %p").lstrip("0")
                action = (self.config.get("per_prayer_actions") or {}).get(
                    p, self.config.get("default_action")
                )
                self.prayer_cards[p].update_data(time_disp, f"{action.title()} · Passed", is_passed=True)

    # ── Button handlers ──
    def _on_pause_clicked(self):
        is_paused = self.btn_pause.isChecked()
        self.btn_pause.setText("▶  Resume Automation" if is_paused else "⏸  Pause Automation")
        self.pause_toggled.emit(is_paused)
        if is_paused:
            self.countdown_label.setText("⏸  Automation Paused")

    def _on_skip_clicked(self):
        self.skip_requested.emit()
        QMessageBox.information(self, "Skipped", "The next scheduled action has been skipped.")

    def _on_trigger_clicked(self):
        reply = QMessageBox.question(
            self, "Trigger Now",
            "Execute the configured action immediately?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            self.trigger_now_requested.emit()
