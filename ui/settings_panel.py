from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QComboBox, QSpinBox, QCheckBox, 
                               QPushButton, QFormLayout, QScrollArea, QGroupBox)
from PySide6.QtCore import Signal
from .widgets import FluentCard

class SettingsPanel(QWidget):
    
    settings_changed = Signal()
    location_detect_requested = Signal()
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        
        main_layout = QVBoxLayout(self)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setSpacing(20)
        
        # Location & Method
        loc_group = QGroupBox("Location & Calculation Method")
        loc_layout = QFormLayout(loc_group)
        
        self.edit_city = QLineEdit(self.config.get("city"))
        self.edit_country = QLineEdit(self.config.get("country"))
        
        self.btn_detect = QPushButton("Auto-Detect Location")
        self.btn_detect.clicked.connect(self.location_detect_requested.emit)
        
        self.combo_method = QComboBox()
        # Adding a few common methods. Real implementation would list all from Aladhan.
        methods = {
            "3": "Muslim World League",
            "2": "ISNA",
            "4": "Umm Al-Qura",
            "5": "Egyptian General Authority"
        }
        for k, v in methods.items():
            self.combo_method.addItem(v, k)
        
        curr_method = str(self.config.get("method"))
        index = self.combo_method.findData(curr_method)
        if index >= 0:
            self.combo_method.setCurrentIndex(index)
            
        self.combo_asr = QComboBox()
        self.combo_asr.addItems(["Standard", "Hanafi"])
        self.combo_asr.setCurrentText(self.config.get("asr_jurisprudence"))
        
        loc_layout.addRow("City:", self.edit_city)
        loc_layout.addRow("Country:", self.edit_country)
        loc_layout.addRow("", self.btn_detect)
        loc_layout.addRow("Method:", self.combo_method)
        loc_layout.addRow("Asr Jurisprudence:", self.combo_asr)
        
        # Actions
        act_group = QGroupBox("Actions & Timing")
        act_layout = QFormLayout(act_group)
        
        actions = ["sleep", "hibernate", "shutdown", "lock", "notification"]
        
        self.combo_default_action = QComboBox()
        self.combo_default_action.addItems(actions)
        self.combo_default_action.setCurrentText(self.config.get("default_action"))
        
        self.spin_alert = QSpinBox()
        self.spin_alert.setRange(0, 120)
        self.spin_alert.setValue(self.config.get("alert_minutes_before"))
        self.spin_alert.setSuffix(" min")
        
        self.chk_snooze = QCheckBox("Enable Snooze prompt")
        self.chk_snooze.setChecked(self.config.get("snooze_enabled"))
        
        self.spin_snooze = QSpinBox()
        self.spin_snooze.setRange(1, 60)
        self.spin_snooze.setValue(self.config.get("snooze_minutes"))
        self.spin_snooze.setSuffix(" min")
        
        act_layout.addRow("Default Action:", self.combo_default_action)
        act_layout.addRow("Alert Before:", self.spin_alert)
        act_layout.addRow("Snooze:", self.chk_snooze)
        act_layout.addRow("Snooze Duration:", self.spin_snooze)
        
        # System Behavior
        sys_group = QGroupBox("System Behavior")
        sys_layout = QVBoxLayout(sys_group)
        
        self.chk_startup = QCheckBox("Launch on Windows startup")
        self.chk_startup.setChecked(self.config.get("launch_on_startup"))
        
        self.chk_minimized = QCheckBox("Start minimized in system tray")
        self.chk_minimized.setChecked(self.config.get("start_minimized"))
        
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["system", "dark", "light"])
        self.combo_theme.setCurrentText(self.config.get("theme"))
        
        sys_layout.addWidget(self.chk_startup)
        sys_layout.addWidget(self.chk_minimized)
        sys_layout_form = QFormLayout()
        sys_layout_form.addRow("Theme:", self.combo_theme)
        sys_layout.addLayout(sys_layout_form)
        
        layout.addWidget(loc_group)
        layout.addWidget(act_group)
        layout.addWidget(sys_group)
        layout.addStretch()
        
        scroll.setWidget(content)
        main_layout.addWidget(scroll)
        
        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Save Settings")
        self.btn_save.setProperty("class", "ActionButton")
        self.btn_save.clicked.connect(self.save_settings)
        
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        
        main_layout.addLayout(btn_layout)
        
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
