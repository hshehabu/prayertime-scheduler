from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QSpinBox, QCheckBox, QPushButton, QFormLayout,
    QScrollArea, QGroupBox,
)
from PySide6.QtCore import Signal


class SettingsPanel(QWidget):
    """Settings view with properly spaced group boxes."""

    settings_changed = Signal()
    location_detect_requested = Signal()

    # Aladhan calculation methods
    METHODS = [
        ("0", "Jafari / Shia Ithna-Ashari"),
        ("1", "University of Islamic Sciences, Karachi"),
        ("2", "Islamic Society of North America (ISNA)"),
        ("3", "Muslim World League"),
        ("4", "Umm Al-Qura University, Makkah"),
        ("5", "Egyptian General Authority of Survey"),
        ("7", "Institute of Geophysics, University of Tehran"),
        ("8", "Gulf Region"),
        ("9", "Kuwait"),
        ("10", "Qatar"),
        ("11", "Majlis Ugama Islam Singapura"),
        ("12", "Union des Organisations Islamiques de France"),
        ("13", "Diyanet İşleri Başkanlığı, Turkey"),
        ("14", "Spiritual Administration of Muslims of Russia"),
        ("15", "Moonsighting Committee Worldwide"),
    ]

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # ── Location & Method ──
        loc_group = QGroupBox("Location && Calculation Method")
        loc_form = QFormLayout()
        loc_form.setSpacing(12)
        loc_form.setContentsMargins(8, 8, 8, 8)

        self.edit_city = QLineEdit(self.config.get("city"))
        self.edit_country = QLineEdit(self.config.get("country"))

        self.btn_detect = QPushButton("🌍  Auto-Detect Location")
        self.btn_detect.clicked.connect(self.location_detect_requested.emit)

        self.combo_method = QComboBox()
        for code, name in self.METHODS:
            self.combo_method.addItem(name, code)
        idx = self.combo_method.findData(str(self.config.get("method")))
        if idx >= 0:
            self.combo_method.setCurrentIndex(idx)

        self.combo_asr = QComboBox()
        self.combo_asr.addItems(["Standard", "Hanafi"])
        self.combo_asr.setCurrentText(self.config.get("asr_jurisprudence"))

        loc_form.addRow("City:", self.edit_city)
        loc_form.addRow("Country:", self.edit_country)
        loc_form.addRow("", self.btn_detect)
        loc_form.addRow("Method:", self.combo_method)
        loc_form.addRow("Asr Jurisprudence:", self.combo_asr)
        loc_group.setLayout(loc_form)

        # ── Actions & Timing ──
        act_group = QGroupBox("Actions && Timing")
        act_form = QFormLayout()
        act_form.setSpacing(12)
        act_form.setContentsMargins(8, 8, 8, 8)

        actions = ["sleep", "hibernate", "shutdown", "lock", "notification"]
        self.combo_default_action = QComboBox()
        self.combo_default_action.addItems(actions)
        self.combo_default_action.setCurrentText(self.config.get("default_action"))

        self.spin_alert = QSpinBox()
        self.spin_alert.setRange(0, 120)
        self.spin_alert.setValue(self.config.get("alert_minutes_before"))
        self.spin_alert.setSuffix(" min")

        self.chk_snooze = QCheckBox("Enable Snooze prompt before action")
        self.chk_snooze.setChecked(self.config.get("snooze_enabled"))

        self.spin_snooze = QSpinBox()
        self.spin_snooze.setRange(1, 60)
        self.spin_snooze.setValue(self.config.get("snooze_minutes"))
        self.spin_snooze.setSuffix(" min")

        act_form.addRow("Default Action:", self.combo_default_action)
        act_form.addRow("Alert Before:", self.spin_alert)
        act_form.addRow("", self.chk_snooze)
        act_form.addRow("Snooze Duration:", self.spin_snooze)
        act_group.setLayout(act_form)

        # ── System Behavior ──
        sys_group = QGroupBox("System Behavior")
        sys_layout = QVBoxLayout()
        sys_layout.setSpacing(12)
        sys_layout.setContentsMargins(8, 8, 8, 8)

        self.chk_startup = QCheckBox("Launch on Windows startup")
        self.chk_startup.setChecked(self.config.get("launch_on_startup"))

        self.chk_minimized = QCheckBox("Start minimized in system tray")
        self.chk_minimized.setChecked(self.config.get("start_minimized"))

        theme_row = QHBoxLayout()
        theme_label = QLabel("Theme:")
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["dark", "light", "system"])
        self.combo_theme.setCurrentText(self.config.get("theme"))
        theme_row.addWidget(theme_label)
        theme_row.addWidget(self.combo_theme, 1)

        sys_layout.addWidget(self.chk_startup)
        sys_layout.addWidget(self.chk_minimized)
        sys_layout.addLayout(theme_row)
        sys_group.setLayout(sys_layout)

        layout.addWidget(loc_group)
        layout.addWidget(act_group)
        layout.addWidget(sys_group)
        layout.addStretch()

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # ── Save button ──
        btn_bar = QHBoxLayout()
        btn_bar.setContentsMargins(20, 8, 20, 12)
        self.btn_save = QPushButton("💾  Save Settings")
        self.btn_save.setProperty("class", "ActionButton")
        self.btn_save.clicked.connect(self.save_settings)
        btn_bar.addStretch()
        btn_bar.addWidget(self.btn_save)
        main_layout.addLayout(btn_bar)

    def set_location(self, city, country):
        self.edit_city.setText(city)
        self.edit_country.setText(country)

    def save_settings(self):
        self.config.set("city", self.edit_city.text())
        self.config.set("country", self.edit_country.text())
        self.config.set("method", int(self.combo_method.currentData()))
        self.config.set("asr_jurisprudence", self.combo_asr.currentText())
        self.config.set("default_action", self.combo_default_action.currentText())
        self.config.set("alert_minutes_before", self.spin_alert.value())
        self.config.set("snooze_enabled", self.chk_snooze.isChecked())
        self.config.set("snooze_minutes", self.spin_snooze.value())
        self.config.set("launch_on_startup", self.chk_startup.isChecked())
        self.config.set("start_minimized", self.chk_minimized.isChecked())
        self.config.set("theme", self.combo_theme.currentText())
        self.settings_changed.emit()
