import json
import os
from pathlib import Path
from typing import Any, Dict

class AppConfig:
    """Manages application settings with JSON persistence."""
    
    DEFAULT_CONFIG = {
        "city": "Addis Ababa",
        "country": "Ethiopia",
        "method": 3,
        "asr_jurisprudence": "Standard",
        "theme": "system",
        "default_action": "sleep",
        "per_prayer_actions": {},
        "alert_minutes_before": 5,
        "snooze_enabled": True,
        "snooze_minutes": 10,
        "launch_on_startup": False,
        "start_minimized": False
    }

    def __init__(self):
        self.app_data_dir = Path(os.environ.get("APPDATA", os.path.expanduser("~"))) / "PrayerTimeScheduler"
        self.app_data_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = self.app_data_dir / "settings.json"
        self._settings = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self) -> None:
        """Load settings from JSON file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                    # Update defaults with loaded values
                    for key, value in loaded_config.items():
                        if key in self._settings:
                            self._settings[key] = value
            except Exception as e:
                print(f"Failed to load config: {e}")
        else:
            self.save()

    def save(self) -> None:
        """Save current settings to JSON file."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=4)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def get(self, key: str) -> Any:
        """Get a configuration value."""
        return self._settings.get(key)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value and save."""
        if key in self._settings:
            self._settings[key] = value
            self.save()

    def get_all(self) -> Dict[str, Any]:
        """Return a copy of all settings."""
        return self._settings.copy()

    def reset_defaults(self) -> None:
        """Reset to default configuration."""
        self._settings = self.DEFAULT_CONFIG.copy()
        self.save()
