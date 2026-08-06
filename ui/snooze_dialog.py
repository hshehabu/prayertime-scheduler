from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QProgressBar
from PySide6.QtCore import Qt, QTimer, Signal


class SnoozeDialog(QDialog):
    """Pre-action snooze/cancel dialog — earth-tone styled."""

    snooze_requested = Signal()
    execute_now_requested = Signal()
    cancel_requested = Signal()

    def __init__(self, prayer_name, action_name, timeout_secs=300, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🕌 Action Imminent")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setFixedSize(440, 210)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                             stop:0 #2A2320, stop:1 #36302C);
                border: 2px solid #C1B090;
                border-radius: 12px;
            }
        """)

        self.timeout_secs = timeout_secs
        self.remaining = timeout_secs

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(10)

        icon = QLabel("🕌")
        icon.setFont(icon.font().__class__("Segoe UI", 26))
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("border: none;")

        self.msg = QLabel(f"PC will <b>{action_name.upper()}</b> for <b>{prayer_name}</b> prayer.")
        self.msg.setAlignment(Qt.AlignCenter)
        self.msg.setStyleSheet("color: #E8E0D8; font-size: 13px; border: none;")

        self.timer_lbl = QLabel(f"Executing in {self.remaining}s …")
        self.timer_lbl.setAlignment(Qt.AlignCenter)
        self.timer_lbl.setStyleSheet("color: #C1B090; font-weight: bold; border: none;")

        self.bar = QProgressBar()
        self.bar.setMaximum(timeout_secs)
        self.bar.setValue(timeout_secs)
        self.bar.setTextVisible(False)
        self.bar.setFixedHeight(6)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)

        btn_style = lambda bg: f"""
            QPushButton {{ background: {bg}; color: white; border: none;
                           border-radius: 8px; padding: 8px 16px; font-weight: bold; }}
            QPushButton:hover {{ opacity: 0.9; }}
        """

        self.btn_cancel = QPushButton("✖  Cancel")
        self.btn_cancel.setStyleSheet("""
            QPushButton { background: #4E4540; color: #E8E0D8; border: 1px solid #5E5550;
                          border-radius: 8px; padding: 8px 16px; }
            QPushButton:hover { border-color: #C1B090; }
        """)
        self.btn_cancel.clicked.connect(self.on_cancel)

        self.btn_snooze = QPushButton("💤  Snooze 10 min")
        self.btn_snooze.setStyleSheet(btn_style("#9C9E58"))
        self.btn_snooze.clicked.connect(self.on_snooze)

        self.btn_now = QPushButton("⚡  Do It Now")
        self.btn_now.setStyleSheet(btn_style("#67504C"))
        self.btn_now.clicked.connect(self.on_now)

        btn_row.addWidget(self.btn_cancel)
        btn_row.addWidget(self.btn_snooze)
        btn_row.addWidget(self.btn_now)

        layout.addWidget(icon)
        layout.addWidget(self.msg)
        layout.addWidget(self.timer_lbl)
        layout.addWidget(self.bar)
        layout.addLayout(btn_row)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(1000)

    def _tick(self):
        self.remaining -= 1
        self.timer_lbl.setText(f"Executing in {self.remaining}s …")
        self.bar.setValue(self.remaining)
        if self.remaining <= 0:
            self._timer.stop()
            self.on_now()

    def on_snooze(self):
        self._timer.stop()
        self.snooze_requested.emit()
        self.accept()

    def on_now(self):
        self._timer.stop()
        self.execute_now_requested.emit()
        self.accept()

    def on_cancel(self):
        self._timer.stop()
        self.cancel_requested.emit()
        self.reject()
