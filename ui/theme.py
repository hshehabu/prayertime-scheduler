from PySide6.QtWidgets import QApplication

# ── Islamic-inspired colour palette ──
#   Dark mode:  midnight blue-black surfaces, gold + emerald accents
#   Light mode: warm ivory surfaces, deep green + gold accents

DARK_BG       = "#0D1117"
DARK_CARD     = "#161B22"
DARK_BORDER   = "#21262D"
GOLD          = "#D4A843"
GOLD_HOVER    = "#E0BE6A"
EMERALD       = "#1FAB6F"
EMERALD_DARK  = "#157A4E"
CREAM         = "#FDF8EE"
IVORY_CARD    = "#FFFFFF"
LIGHT_BORDER  = "#D9CEB2"
DEEP_GREEN    = "#145A32"
TEXT_LIGHT    = "#E6EDF3"
TEXT_DARK     = "#1C1C1C"


COMMON_STYLE = """
    * {{
        font-family: 'Segoe UI Variable', 'Segoe UI', sans-serif;
    }}
    QScrollBar:vertical {{
        border: none; background: transparent; width: 8px;
    }}
    QScrollBar::handle:vertical {{
        background-color: {gold}; min-height: 20px; border-radius: 4px;
    }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        border: none; background: none;
    }}
"""


DARK_STYLE = COMMON_STYLE.format(gold=GOLD) + f"""
    QWidget {{
        background-color: {DARK_BG};
        color: {TEXT_LIGHT};
    }}

    /* ── Cards ── */
    .FluentCard, QGroupBox {{
        background-color: {DARK_CARD};
        border: 1px solid {DARK_BORDER};
        border-radius: 12px;
    }}
    QGroupBox::title {{
        color: {GOLD};
        subcontrol-origin: margin;
        padding: 4px 12px;
        font-weight: bold;
    }}

    /* ── Prayer Card (active) ── */
    .ActivePrayerCard {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                     stop:0 {EMERALD_DARK}, stop:1 {EMERALD});
        border: 2px solid {GOLD};
        border-radius: 12px;
        color: white;
    }}
    .PassedPrayerCard {{
        background-color: {DARK_CARD};
        border: 1px solid {DARK_BORDER};
        border-radius: 12px;
        opacity: 0.6;
    }}

    /* ── Buttons ── */
    QPushButton {{
        background-color: {DARK_CARD};
        border: 1px solid {DARK_BORDER};
        border-radius: 8px;
        padding: 8px 18px;
        color: {TEXT_LIGHT};
        font-weight: 500;
    }}
    QPushButton:hover {{
        background-color: #21262D;
        border-color: {GOLD};
    }}
    QPushButton:pressed {{
        background-color: #0D1117;
    }}

    .ActionButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                     stop:0 {EMERALD_DARK}, stop:1 {EMERALD});
        border: none;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
    }}
    .ActionButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                     stop:0 {EMERALD}, stop:1 {GOLD});
    }}

    /* ── Inputs ── */
    QLineEdit, QComboBox, QSpinBox {{
        background-color: {DARK_CARD};
        border: 1px solid {DARK_BORDER};
        border-radius: 6px;
        padding: 6px 10px;
        color: {TEXT_LIGHT};
    }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
        border: 1px solid {GOLD};
    }}

    /* ── Tabs ── */
    QTabWidget::pane {{
        border: 1px solid {DARK_BORDER};
        background: {DARK_BG};
        border-radius: 12px;
    }}
    QTabBar::tab {{
        background: {DARK_CARD};
        padding: 10px 20px;
        border: 1px solid {DARK_BORDER};
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        margin-right: 2px;
        color: {TEXT_LIGHT};
    }}
    QTabBar::tab:selected {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                     stop:0 {EMERALD_DARK}, stop:1 {EMERALD});
        color: white;
        border-bottom: 2px solid {GOLD};
    }}

    /* ── Hero / Countdown ── */
    .HeroTime {{
        color: {TEXT_LIGHT};
    }}
    .HeroCountdown {{
        color: {GOLD};
    }}
    .LocationLabel {{
        color: #8B949E;
    }}

    /* ── Progress bar (snooze dialog) ── */
    QProgressBar {{
        background: {DARK_CARD};
        border: 1px solid {DARK_BORDER};
        border-radius: 6px;
        height: 8px;
    }}
    QProgressBar::chunk {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                     stop:0 {EMERALD}, stop:1 {GOLD});
        border-radius: 6px;
    }}

    /* ── Check / Radio ── */
    QCheckBox {{
        spacing: 8px;
        color: {TEXT_LIGHT};
    }}
    QCheckBox::indicator {{
        width: 18px; height: 18px;
        border-radius: 4px;
        border: 1px solid {DARK_BORDER};
        background: {DARK_CARD};
    }}
    QCheckBox::indicator:checked {{
        background: {EMERALD};
        border-color: {GOLD};
    }}
"""


LIGHT_STYLE = COMMON_STYLE.format(gold="#B8860B") + f"""
    QWidget {{
        background-color: {CREAM};
        color: {TEXT_DARK};
    }}

    .FluentCard, QGroupBox {{
        background-color: {IVORY_CARD};
        border: 1px solid {LIGHT_BORDER};
        border-radius: 12px;
    }}
    QGroupBox::title {{
        color: {DEEP_GREEN};
        subcontrol-origin: margin;
        padding: 4px 12px;
        font-weight: bold;
    }}

    .ActivePrayerCard {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                     stop:0 {DEEP_GREEN}, stop:1 {EMERALD});
        border: 2px solid #B8860B;
        border-radius: 12px;
        color: white;
    }}
    .PassedPrayerCard {{
        background-color: #F0EBE0;
        border: 1px solid {LIGHT_BORDER};
        border-radius: 12px;
    }}

    QPushButton {{
        background-color: {IVORY_CARD};
        border: 1px solid {LIGHT_BORDER};
        border-radius: 8px;
        padding: 8px 18px;
        color: {TEXT_DARK};
        font-weight: 500;
    }}
    QPushButton:hover {{
        background-color: #F5EDD8;
        border-color: {DEEP_GREEN};
    }}

    .ActionButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                     stop:0 {DEEP_GREEN}, stop:1 {EMERALD});
        border: none;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
    }}
    .ActionButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                     stop:0 {EMERALD}, stop:1 #B8860B);
    }}

    QLineEdit, QComboBox, QSpinBox {{
        background-color: {IVORY_CARD};
        border: 1px solid {LIGHT_BORDER};
        border-radius: 6px;
        padding: 6px 10px;
        color: {TEXT_DARK};
    }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
        border: 1px solid {DEEP_GREEN};
    }}

    QTabWidget::pane {{
        border: 1px solid {LIGHT_BORDER};
        background: {CREAM};
        border-radius: 12px;
    }}
    QTabBar::tab {{
        background: {IVORY_CARD};
        padding: 10px 20px;
        border: 1px solid {LIGHT_BORDER};
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
        margin-right: 2px;
    }}
    QTabBar::tab:selected {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                     stop:0 {DEEP_GREEN}, stop:1 {EMERALD});
        color: white;
        border-bottom: 2px solid #B8860B;
    }}

    .HeroTime {{
        color: {DEEP_GREEN};
    }}
    .HeroCountdown {{
        color: #B8860B;
    }}
    .LocationLabel {{
        color: #6B6B6B;
    }}

    QProgressBar {{
        background: #E8E0D0;
        border: 1px solid {LIGHT_BORDER};
        border-radius: 6px;
        height: 8px;
    }}
    QProgressBar::chunk {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                     stop:0 {DEEP_GREEN}, stop:1 #B8860B);
        border-radius: 6px;
    }}

    QCheckBox {{
        spacing: 8px;
    }}
    QCheckBox::indicator {{
        width: 18px; height: 18px;
        border-radius: 4px;
        border: 1px solid {LIGHT_BORDER};
        background: {IVORY_CARD};
    }}
    QCheckBox::indicator:checked {{
        background: {DEEP_GREEN};
        border-color: #B8860B;
    }}
"""


class ThemeManager:
    """Applies dark / light / system theme."""

    @classmethod
    def apply_theme(cls, theme_mode: str):
        app = QApplication.instance()
        if not app:
            return

        if theme_mode == "system":
            theme_mode = "dark"  # Fallback; real detection would read Windows registry

        if theme_mode == "dark":
            app.setStyleSheet(DARK_STYLE)
        else:
            app.setStyleSheet(LIGHT_STYLE)
