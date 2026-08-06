import sys
import ctypes
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, QPoint, QTimer, Signal
from PySide6.QtGui import QFont, QScreen, QGuiApplication


class FloatingWidget(QWidget):
    """Desktop widget with two modes: desktop (behind apps) and overlay (on top)."""

    show_main_requested = Signal()
    DESKTOP_SIZE = (300, 110)
    OVERLAY_SIZE = (220, 80)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._desktop_mode = True
        self._drag_pos = QPoint()

        # Start in desktop mode (no always-on-top)
        self._apply_desktop_flags()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(*self.DESKTOP_SIZE)

        # Container
        self.container = QWidget(self)
        self._update_container_geometry()

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(14, 8, 14, 8)
        layout.setSpacing(2)

        # Top row: prayer label + toggle button
        top_row = QHBoxLayout()
        top_row.setSpacing(4)

        self.prayer_label = QLabel("🕌  Next Prayer")
        self.prayer_label.setFont(QFont("Segoe UI Variable", 10, QFont.Bold))
        self.prayer_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.toggle_btn = QPushButton("📌")
        self.toggle_btn.setFixedSize(26, 26)
        self.toggle_btn.setToolTip("Toggle: Desktop / Overlay mode")
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_mode)

        top_row.addWidget(self.prayer_label, 1)
        top_row.addWidget(self.toggle_btn)

        self.countdown_label = QLabel("--:--:--")
        self.countdown_label.setFont(QFont("Segoe UI Variable", 22, QFont.Bold))
        self.countdown_label.setAlignment(Qt.AlignCenter)

        self.action_label = QLabel("")
        self.action_label.setAlignment(Qt.AlignCenter)
        action_font = QFont("Segoe UI Variable", 8)
        self.action_label.setFont(action_font)

        layout.addLayout(top_row)
        layout.addWidget(self.countdown_label)
        layout.addWidget(self.action_label)

        self._apply_styles()

        # Timer to enforce desktop z-order
        self._z_timer = QTimer(self)
        self._z_timer.timeout.connect(self._enforce_desktop_z)
        self._z_timer.start(2000)

        # Position bottom-right of screen
        self._position_default()

    # ── Modes ────────────────────────────────────────────────────────────────

    def _apply_desktop_flags(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowDoesNotAcceptFocus)

    def _apply_overlay_flags(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

    def toggle_mode(self):
        was_visible = self.isVisible()
        pos = self.pos()

        if self._desktop_mode:
            # Switch to overlay (on-top, smaller)
            self._desktop_mode = False
            self._apply_overlay_flags()
            self.setFixedSize(*self.OVERLAY_SIZE)
            self._update_container_geometry()
            self.toggle_btn.setToolTip("Switch to Desktop mode")
            self.toggle_btn.setText("🖥️")
            self._adjust_font_sizes(small=True)
        else:
            # Switch to desktop (behind apps, larger)
            self._desktop_mode = True
            self._apply_desktop_flags()
            self.setFixedSize(*self.DESKTOP_SIZE)
            self._update_container_geometry()
            self.toggle_btn.setToolTip("Switch to Overlay mode")
            self.toggle_btn.setText("📌")
            self._adjust_font_sizes(small=False)

        self._apply_styles()
        self.move(pos)
        if was_visible:
            self.show()
            if self._desktop_mode:
                self._enforce_desktop_z()

    def _adjust_font_sizes(self, small: bool):
        if small:
            self.prayer_label.setFont(QFont("Segoe UI Variable", 8, QFont.Bold))
            self.countdown_label.setFont(QFont("Segoe UI Variable", 16, QFont.Bold))
            self.action_label.setFont(QFont("Segoe UI Variable", 7))
            self.container.layout().setContentsMargins(10, 6, 10, 6)
        else:
            self.prayer_label.setFont(QFont("Segoe UI Variable", 10, QFont.Bold))
            self.countdown_label.setFont(QFont("Segoe UI Variable", 22, QFont.Bold))
            self.action_label.setFont(QFont("Segoe UI Variable", 8))
            self.container.layout().setContentsMargins(14, 8, 14, 8)

    def _update_container_geometry(self):
        w, h = (self.OVERLAY_SIZE if not self._desktop_mode else self.DESKTOP_SIZE)
        self.container.setGeometry(0, 0, w, h)

    def _enforce_desktop_z(self):
        """In desktop mode, push window to the bottom of the z-order."""
        if not self._desktop_mode or not self.isVisible():
            return
        if sys.platform == "win32":
            try:
                hwnd = int(self.winId())
                HWND_BOTTOM = 1
                SWP = 0x0002 | 0x0001 | 0x0010  # NOMOVE | NOSIZE | NOACTIVATE
                ctypes.windll.user32.SetWindowPos(hwnd, HWND_BOTTOM, 0, 0, 0, 0, SWP)
            except Exception:
                pass

    def _position_default(self):
        screen = QGuiApplication.primaryScreen()
        if screen:
            geo = screen.availableGeometry()
            x = geo.right() - self.width() - 20
            y = geo.bottom() - self.height() - 20
            self.move(x, y)

    # ── Styles ───────────────────────────────────────────────────────────────

    def _apply_styles(self):
        self.container.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                             stop:0 #2A2320, stop:1 #36302C);
                border: 1px solid #C1B090;
                border-radius: 12px;
            }
        """)
        self.prayer_label.setStyleSheet("color: #C1B090; border: none;")
        self.countdown_label.setStyleSheet("color: #E8E0D8; border: none;")
        self.action_label.setStyleSheet("color: #9C9E58; border: none;")
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: 1px solid #4E4540;
                border-radius: 4px;
                font-size: 12px;
                color: #C1B090;
            }
            QPushButton:hover { border-color: #C1B090; background: #36302C; }
        """)

    # ── Data ─────────────────────────────────────────────────────────────────

    def update_countdown(self, secs_left, prayer_name, action_name):
        h, m, s = secs_left // 3600, (secs_left % 3600) // 60, secs_left % 60
        self.prayer_label.setText(f"🕌  {prayer_name}")
        self.countdown_label.setText(f"{h:02d}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}")
        self.action_label.setText(f"{action_name.title()} · {self._friendly(secs_left)}")

    def set_no_upcoming(self):
        self.prayer_label.setText("🕌  All Done")
        self.countdown_label.setText("✓")
        self.action_label.setText("See you tomorrow, In Shaa Allah")

    def set_paused(self):
        self.prayer_label.setText("⏸  Paused")
        self.countdown_label.setText("--:--")
        self.action_label.setText("")

    @staticmethod
    def _friendly(s):
        return f"{s // 3600}h {(s % 3600) // 60}m left" if s > 3600 else f"{s // 60}m {s % 60}s left"

    # ── Dragging ─────────────────────────────────────────────────────────────

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self._desktop_mode:
            self._enforce_desktop_z()

    def mouseDoubleClickEvent(self, event):
        self.show_main_requested.emit()

    def showEvent(self, event):
        super().showEvent(event)
        if self._desktop_mode:
            QTimer.singleShot(100, self._enforce_desktop_z)
