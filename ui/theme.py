from PySide6.QtWidgets import QApplication

# ─── Muted Earth-Tone Palette (from "Study Hard") ───
# Primary:  #67504C (dark brown-mauve)    #C1B090 (warm tan/camel)
# Neutral:  #DFE1E5 (cool light gray)    #C0B08C (warm khaki)
# Accent:   #9C9E58 (olive/sage green)
# Text:     #1B1B1B (near black)

# Dark-mode derived tones
_D_BG        = "#2A2320"
_D_CARD      = "#36302C"
_D_BORDER    = "#4E4540"
_D_TEXT      = "#E8E0D8"
_D_MUTED     = "#9A8E84"

# Light-mode tones
_L_BG        = "#F2EDE8"
_L_CARD      = "#FFFFFF"
_L_BORDER    = "#D4C9B8"
_L_TEXT      = "#1B1B1B"
_L_MUTED     = "#7A6E64"

# Shared accent colours
TAN          = "#C1B090"
BROWN        = "#67504C"
OLIVE        = "#9C9E58"
OLIVE_HOVER  = "#B0B268"
KHAKI        = "#C0B08C"


# ── Shared scrollbar + font ──────────────────────────────────────────────────
_COMMON = """
* {{
    font-family: 'Segoe UI Variable', 'Segoe UI', sans-serif;
}}
QScrollBar:vertical {{
    border: none; background: transparent; width: 8px;
}}
QScrollBar::handle:vertical {{
    background-color: {tan}; min-height: 20px; border-radius: 4px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    border: none; background: none;
}}
QScrollArea {{ border: none; }}
"""


# ═══════════════════════════════  DARK  ═══════════════════════════════════════
DARK_STYLE = _COMMON.format(tan=TAN) + f"""

/* ── Base ── */
QWidget {{
    background-color: {_D_BG};
    color: {_D_TEXT};
}}

/* ── Group Boxes (settings sections) ── */
QGroupBox {{
    background-color: {_D_CARD};
    border: 1px solid {_D_BORDER};
    border-radius: 10px;
    margin-top: 20px;
    padding: 24px 16px 16px 16px;
    font-weight: bold;
    font-size: 13px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    top: 4px;
    padding: 2px 8px;
    color: {TAN};
    background-color: {_D_CARD};
    border-radius: 4px;
}}

/* ── Cards ── */
.FluentCard {{
    background-color: {_D_CARD};
    border: 1px solid {_D_BORDER};
    border-radius: 10px;
}}

.ActivePrayerCard {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                 stop:0 #4A4230, stop:1 #5C5438);
    border: 2px solid {TAN};
    border-radius: 10px;
    color: {_D_TEXT};
}}
.PassedPrayerCard {{
    background-color: {_D_CARD};
    border: 1px solid {_D_BORDER};
    border-radius: 10px;
    color: {_D_MUTED};
}}

/* ── Buttons ── */
QPushButton {{
    background-color: {_D_CARD};
    border: 1px solid {_D_BORDER};
    border-radius: 8px;
    padding: 8px 18px;
    color: {_D_TEXT};
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: #443D38;
    border-color: {TAN};
}}
QPushButton:pressed {{
    background-color: #2A2320;
}}

.ActionButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                 stop:0 {OLIVE}, stop:1 {OLIVE_HOVER});
    border: none;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 10px 20px;
}}
.ActionButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                 stop:0 {OLIVE_HOVER}, stop:1 {TAN});
}}

/* ── Inputs ── */
QLineEdit, QComboBox, QSpinBox {{
    background-color: #2A2320;
    border: 1px solid {_D_BORDER};
    border-radius: 6px;
    padding: 6px 10px;
    color: {_D_TEXT};
    min-height: 20px;
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border: 1px solid {TAN};
}}
QComboBox::drop-down {{
    border: none;
    width: 24px;
}}
QComboBox QAbstractItemView {{
    background-color: {_D_CARD};
    border: 1px solid {_D_BORDER};
    color: {_D_TEXT};
    selection-background-color: {OLIVE};
}}

/* ── Tabs ── */
QTabWidget::pane {{
    border: 1px solid {_D_BORDER};
    background: {_D_BG};
    border-radius: 0 0 10px 10px;
    top: -1px;
}}
QTabBar::tab {{
    background: {_D_CARD};
    padding: 10px 22px;
    border: 1px solid {_D_BORDER};
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 2px;
    color: {_D_MUTED};
    font-weight: 500;
}}
QTabBar::tab:selected {{
    background: {BROWN};
    color: {_D_TEXT};
    border-color: {BROWN};
}}
QTabBar::tab:hover:!selected {{
    background: #443D38;
    color: {_D_TEXT};
}}

/* ── Labels ── */
.HeroTime {{ color: {_D_TEXT}; }}
.HeroCountdown {{ color: {TAN}; }}
.LocationLabel {{ color: {_D_MUTED}; }}

/* ── Progress bar ── */
QProgressBar {{
    background: {_D_CARD};
    border: 1px solid {_D_BORDER};
    border-radius: 4px;
    height: 6px;
    text-align: center;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                 stop:0 {OLIVE}, stop:1 {TAN});
    border-radius: 4px;
}}

/* ── Checkbox ── */
QCheckBox {{ spacing: 8px; color: {_D_TEXT}; }}
QCheckBox::indicator {{
    width: 18px; height: 18px; border-radius: 4px;
    border: 1px solid {_D_BORDER}; background: {_D_BG};
}}
QCheckBox::indicator:checked {{
    background: {OLIVE}; border-color: {TAN};
}}

/* ── Form labels ── */
QLabel {{ background: transparent; }}
"""


# ═══════════════════════════════  LIGHT  ══════════════════════════════════════
LIGHT_STYLE = _COMMON.format(tan=BROWN) + f"""

QWidget {{
    background-color: {_L_BG};
    color: {_L_TEXT};
}}

QGroupBox {{
    background-color: {_L_CARD};
    border: 1px solid {_L_BORDER};
    border-radius: 10px;
    margin-top: 20px;
    padding: 24px 16px 16px 16px;
    font-weight: bold;
    font-size: 13px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    top: 4px;
    padding: 2px 8px;
    color: {BROWN};
    background-color: {_L_CARD};
    border-radius: 4px;
}}

.FluentCard {{
    background-color: {_L_CARD};
    border: 1px solid {_L_BORDER};
    border-radius: 10px;
}}
.ActivePrayerCard {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                 stop:0 #D9CEB2, stop:1 {TAN});
    border: 2px solid {BROWN};
    border-radius: 10px;
    color: {_L_TEXT};
}}
.PassedPrayerCard {{
    background-color: #EDE8E2;
    border: 1px solid {_L_BORDER};
    border-radius: 10px;
    color: {_L_MUTED};
}}

QPushButton {{
    background-color: {_L_CARD};
    border: 1px solid {_L_BORDER};
    border-radius: 8px;
    padding: 8px 18px;
    color: {_L_TEXT};
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: #E8E0D6;
    border-color: {BROWN};
}}

.ActionButton {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                 stop:0 {BROWN}, stop:1 {OLIVE});
    border: none; color: white; font-weight: bold;
    border-radius: 8px; padding: 10px 20px;
}}
.ActionButton:hover {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                 stop:0 {OLIVE}, stop:1 {TAN});
}}

QLineEdit, QComboBox, QSpinBox {{
    background-color: {_L_CARD};
    border: 1px solid {_L_BORDER};
    border-radius: 6px;
    padding: 6px 10px;
    color: {_L_TEXT};
    min-height: 20px;
}}
QLineEdit:focus, QComboBox:focus, QSpinBox:focus {{
    border: 1px solid {BROWN};
}}
QComboBox::drop-down {{ border: none; width: 24px; }}
QComboBox QAbstractItemView {{
    background-color: {_L_CARD};
    border: 1px solid {_L_BORDER};
    color: {_L_TEXT};
    selection-background-color: {TAN};
}}

QTabWidget::pane {{
    border: 1px solid {_L_BORDER};
    background: {_L_BG};
    border-radius: 0 0 10px 10px;
    top: -1px;
}}
QTabBar::tab {{
    background: {_L_CARD};
    padding: 10px 22px;
    border: 1px solid {_L_BORDER};
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 2px;
    color: {_L_MUTED};
    font-weight: 500;
}}
QTabBar::tab:selected {{
    background: {BROWN};
    color: white;
    border-color: {BROWN};
}}
QTabBar::tab:hover:!selected {{
    background: #E8E0D6;
    color: {_L_TEXT};
}}

.HeroTime {{ color: {BROWN}; }}
.HeroCountdown {{ color: {OLIVE}; }}
.LocationLabel {{ color: {_L_MUTED}; }}

QProgressBar {{
    background: #E8E0D6;
    border: 1px solid {_L_BORDER};
    border-radius: 4px; height: 6px;
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
                 stop:0 {BROWN}, stop:1 {OLIVE});
    border-radius: 4px;
}}

QCheckBox {{ spacing: 8px; }}
QCheckBox::indicator {{
    width: 18px; height: 18px; border-radius: 4px;
    border: 1px solid {_L_BORDER}; background: {_L_CARD};
}}
QCheckBox::indicator:checked {{
    background: {OLIVE}; border-color: {BROWN};
}}

QLabel {{ background: transparent; }}
"""


class ThemeManager:
    """Applies muted earth-tone dark / light / system theme."""

    @classmethod
    def apply_theme(cls, theme_mode: str):
        app = QApplication.instance()
        if not app:
            return
        if theme_mode == "system":
            theme_mode = "dark"
        app.setStyleSheet(DARK_STYLE if theme_mode == "dark" else LIGHT_STYLE)
