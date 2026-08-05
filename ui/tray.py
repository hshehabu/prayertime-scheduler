from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Signal, QObject

class SystemTrayManager(QObject):
    
    show_requested = Signal()
    exit_requested = Signal()
    pause_toggled = Signal(bool)
    
    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.icon = QIcon(icon_path)
        
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setToolTip("PrayerTime Scheduler")
        
        self.menu = QMenu()
        
        self.status_action = QAction("Status: Initializing...", self.menu)
        self.status_action.setEnabled(False)
        self.menu.addAction(self.status_action)
        self.menu.addSeparator()
        
        self.pause_action = QAction("Pause Automation", self.menu)
        self.pause_action.setCheckable(True)
        self.pause_action.triggered.connect(self._on_pause_triggered)
        self.menu.addAction(self.pause_action)
        
        self.show_action = QAction("Settings / Dashboard", self.menu)
        self.show_action.triggered.connect(self.show_requested.emit)
        self.menu.addAction(self.show_action)
        self.menu.addSeparator()
        
        self.exit_action = QAction("Exit", self.menu)
        self.exit_action.triggered.connect(self.exit_requested.emit)
        self.menu.addAction(self.exit_action)
        
        self.tray.setContextMenu(self.menu)
        self.tray.activated.connect(self._on_activated)
        
    def show(self):
        self.tray.show()
        
    def hide(self):
        self.tray.hide()
        
    def update_tooltip(self, text):
        self.tray.setToolTip(text)
        
    def update_status(self, text):
        self.status_action.setText(text)
        
    def show_toast(self, title, message, duration_ms=5000):
        self.tray.showMessage(title, message, QSystemTrayIcon.Information, duration_ms)
        
    def set_paused_state(self, is_paused):
        self.pause_action.setChecked(is_paused)
        
    def _on_pause_triggered(self, checked):
        self.pause_toggled.emit(checked)
        
    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_requested.emit()
