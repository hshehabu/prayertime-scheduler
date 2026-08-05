from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt


class FluentCard(QFrame):
    """Base card with Fluent/Islamic style."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setProperty("class", "FluentCard")
        self.setFrameShape(QFrame.StyledPanel)


class PrayerTimeCard(FluentCard):
    """Displays a single prayer: name, time, status, and action badge."""

    # Islamic prayer emoji/symbols
    PRAYER_ICONS = {
        "Fajr": "🌅",
        "Dhuhr": "☀️",
        "Asr": "🌤️",
        "Maghrib": "🌇",
        "Isha": "🌙",
    }

    def __init__(self, prayer_name, parent=None):
        super().__init__(parent)
        self.prayer_name = prayer_name

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 18, 16, 18)
        layout.setSpacing(6)

        # Icon + Name row
        icon = self.PRAYER_ICONS.get(prayer_name, "🕌")
        self.icon_label = QLabel(icon)
        icon_font = self.icon_label.font()
        icon_font.setPointSize(22)
        self.icon_label.setFont(icon_font)
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.name_label = QLabel(prayer_name)
        name_font = self.name_label.font()
        name_font.setPointSize(11)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        self.name_label.setAlignment(Qt.AlignCenter)

        self.time_label = QLabel("--:--")
        time_font = self.time_label.font()
        time_font.setPointSize(20)
        time_font.setBold(True)
        self.time_label.setFont(time_font)
        self.time_label.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("")
        status_font = self.status_label.font()
        status_font.setPointSize(8)
        self.status_label.setFont(status_font)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.name_label)
        layout.addStretch()
        layout.addWidget(self.time_label)
        layout.addStretch()
        layout.addWidget(self.status_label)

        self.setMinimumSize(130, 180)

    def update_data(self, time_str, status_text, is_active=False, is_passed=False):
        self.time_label.setText(time_str)
        self.status_label.setText(status_text)

        if is_active:
            self.setProperty("class", "ActivePrayerCard")
        elif is_passed:
            self.setProperty("class", "PassedPrayerCard")
        else:
            self.setProperty("class", "FluentCard")

        # Force style refresh
        self.style().unpolish(self)
        self.style().polish(self)


class ActionButton(QPushButton):
    """Styled action button with Islamic gradient."""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("class", "ActionButton")
        self.setCursor(Qt.PointingHandCursor)
