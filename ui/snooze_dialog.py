from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QProgressBar
from PySide6.QtCore import Qt, QTimer, Signal


class SnoozeDialog(QDialog):
    """Pre-action dialog with snooze, execute-now, and cancel options."""

    snooze_requested = Signal()
    execute_now_requested = Signal()
    cancel_requested = Signal()

    def __init__(self, prayer_name, action_name, timeout_secs=300, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🕌 Action Imminent")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setFixedSize(440, 220)
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                             stop:0 #0D1117, stop:1 #161B22);
                border: 2px solid #D4A843;
                border-radius: 14px;
            }
        """)

        self.timeout_secs = timeout_secs
        self.remaining = timeout_secs

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(12)

        # Icon + message
        icon_label = QLabel("🕌")
        icon_font = icon_label.font()
        icon_font.setPointSize(28)
        icon_label.setFont(icon_font)
        icon_label.setAlignment(Qt.AlignCenter)

        self.msg_label = QLabel(
            f"PC will <b>{action_name.upper()}</b> for <b>{prayer_name}</b> prayer."
        )
        msg_font = self.msg_label.font()
        msg_font.setPointSize(12)
        self.msg_label.setFont(msg_font)
        self.msg_label.setAlignment(Qt.AlignCenter)
        self.msg_label.setStyleSheet("color: #E6EDF3;")

        self.timer_label = QLabel(f"Executing in {self.remaining} seconds...")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("color: #D4A843; font-weight: bold;")

        self.progress = QProgressBar()
        self.progress.setMaximum(timeout_secs)
        self.progress.setValue(timeout_secs)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(6)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.btn_cancel = QPushButton("✖  Cancel")
        self.btn_cancel.setStyleSheet("""
            QPushButton { background: #21262D; color: #E6EDF3; border: 1px solid #30363D;
                          border-radius: 8px; padding: 8px 16px; }
            QPushButton:hover { border-color: #D4A843; }
        """)
        self.btn_cancel.clicked.connect(self.on_cancel)

        self.btn_snooze = QPushButton("💤  Snooze 10 min")
        self.btn_snooze.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                          stop:0 #B8860B, stop:1 #D4A843);
                          color: white; border: none; border-radius: 8px; padding: 8px 16px;
                          font-weight: bold; }
            QPushButton:hover { background: #D4A843; }
        """)
        self.btn_snooze.clicked.connect(self.on_snooze)

        self.btn_now = QPushButton("⚡  Do It Now")
        self.btn_now.setStyleSheet("""
            QPushButton { background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                          stop:0 #157A4E, stop:1 #1FAB6F);
                          color: white; border: none; border-radius: 8px; padding: 8px 16px;
                          font-weight: bold; }
            QPushButton:hover { background: #1FAB6F; }
        """)
        self.btn_now.clicked.connect(self.on_now)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_snooze)
        btn_layout.addWidget(self.btn_now)

        layout.addWidget(icon_label)
        layout.addWidget(self.msg_label)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.progress)
        layout.addLayout(btn_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(1000)

    def tick(self):
        self.remaining -= 1
        self.timer_label.setText(f"Executing in {self.remaining} seconds...")
        self.progress.setValue(self.remaining)
        if self.remaining <= 0:
            self.timer.stop()
            self.on_now()

    def on_snooze(self):
        self.timer.stop()
        self.snooze_requested.emit()
        self.accept()

    def on_now(self):
        self.timer.stop()
        self.execute_now_requested.emit()
        self.accept()

    def on_cancel(self):
        self.timer.stop()
        self.cancel_requested.emit()
        self.reject()
