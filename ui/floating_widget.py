from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QPoint, Signal
from PySide6.QtGui import QFont


class FloatingWidget(QWidget):
    """Small always-on-top desktop overlay showing countdown to next prayer."""

    show_main_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool  # Hides from taskbar
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(280, 100)
        self._drag_pos = QPoint()

        # Container with styled background
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, 280, 100)
        self.container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                             stop:0 #0D1117, stop:1 #161B22);
                border: 1px solid #D4A843;
                border-radius: 14px;
            }
        """)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(4)

        self.prayer_label = QLabel("🕌  Next Prayer")
        self.prayer_label.setStyleSheet("color: #D4A843; border: none; font-weight: bold;")
        prayer_font = QFont("Segoe UI Variable", 10)
        prayer_font.setBold(True)
        self.prayer_label.setFont(prayer_font)
        self.prayer_label.setAlignment(Qt.AlignCenter)

        self.countdown_label = QLabel("--:--:--")
        self.countdown_label.setStyleSheet("color: #FFFFFF; border: none;")
        cd_font = QFont("Segoe UI Variable", 20)
        cd_font.setBold(True)
        self.countdown_label.setFont(cd_font)
        self.countdown_label.setAlignment(Qt.AlignCenter)

        self.action_label = QLabel("")
        self.action_label.setStyleSheet("color: #1FAB6F; border: none; font-size: 9px;")
        self.action_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.prayer_label)
        layout.addWidget(self.countdown_label)
        layout.addWidget(self.action_label)

    def update_countdown(self, secs_left, prayer_name, action_name):
        hours = secs_left // 3600
        minutes = (secs_left % 3600) // 60
        seconds = secs_left % 60

        self.prayer_label.setText(f"🕌  {prayer_name}")
        if hours > 0:
            self.countdown_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        else:
            self.countdown_label.setText(f"{minutes:02d}:{seconds:02d}")
        self.action_label.setText(f"{action_name.title()} · {self._friendly_time(secs_left)}")

    def set_no_upcoming(self):
        self.prayer_label.setText("🕌  All Prayers Done")
        self.countdown_label.setText("✓")
        self.action_label.setText("See you tomorrow, In Shaa Allah")

    def set_paused(self):
        self.prayer_label.setText("⏸  Paused")
        self.countdown_label.setText("--:--")
        self.action_label.setText("")

    @staticmethod
    def _friendly_time(secs):
        if secs > 3600:
            return f"{secs // 3600}h {(secs % 3600) // 60}m left"
        return f"{secs // 60}m {secs % 60}s left"

    # ── Dragging ──
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseDoubleClickEvent(self, event):
        self.show_main_requested.emit()
