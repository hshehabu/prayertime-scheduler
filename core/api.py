import requests
from datetime import datetime
import json
import logging
import re
from pathlib import Path
from PySide6.QtCore import QObject, Signal, QThread
from typing import Dict, Optional


class PrayerTimeAPI(QObject):
    """Fetches prayer times from the Aladhan API and handles caching."""

    times_fetched = Signal(dict)
    fetch_failed = Signal(str)
    location_detected = Signal(str, str)

    API_URL = "https://api.aladhan.com/v1/timingsByCity"
    MAX_RETRIES = 3

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.cache_file = self.config.app_data_dir / "prayer_times_cache.json"
        self._thread = None
        self._loc_thread = None

    def fetch_times_async(self):
        """Starts fetching in a background thread."""
        api = self

        class FetchThread(QThread):
            def __init__(self):
                super().__init__()

            def run(self):
                times = api.get_prayer_times()
                if times:
                    api.times_fetched.emit(times)
                else:
                    api.fetch_failed.emit("Could not fetch prayer times. Check your internet connection and location settings.")

        self._thread = FetchThread()
        self._thread.start()

    def auto_detect_location_async(self):
        """Starts location detection in a background thread."""
        api = self

        class LocationThread(QThread):
            def __init__(self):
                super().__init__()

            def run(self):
                try:
                    response = requests.get("http://ip-api.com/json/", timeout=5)
                    response.raise_for_status()
                    data = response.json()
                    city = data.get("city", "")
                    country = data.get("country", "")
                    if city and country:
                        api.location_detected.emit(city, country)
                    else:
                        api.fetch_failed.emit("Location format invalid.")
                except Exception as e:
                    api.fetch_failed.emit(f"Failed to detect location: {e}")

        self._loc_thread = LocationThread()
        self._loc_thread.start()

    @staticmethod
    def _clean_time_string(time_str: str) -> str:
        """Strip timezone abbreviation from API response, e.g. '18:46 (EAT)' → '18:46'."""
        cleaned = time_str.split("(")[0].strip()
        # Also handle any other non-digit/colon characters
        match = re.match(r"(\d{1,2}:\d{2})", cleaned)
        return match.group(1) if match else cleaned

    def _load_cached_times(self) -> Optional[Dict[str, datetime]]:
        """Load prayer times from cache, ensuring datetimes use today's date."""
        try:
            if not self.cache_file.exists():
                return None
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cache_data = json.load(f)

            cached_date = datetime.strptime(cache_data["date"], "%Y-%m-%d").date()
            if cached_date != datetime.now().date():
                return None

            today = datetime.now().date()
            return {
                prayer: datetime.combine(today, datetime.strptime(time_str, "%H:%M").time())
                for prayer, time_str in cache_data["times"].items()
            }
        except Exception as e:
            logging.warning(f"Cache load failed: {e}")
            return None

    def _save_cached_times(self, prayer_times: Dict[str, datetime]) -> None:
        try:
            cache_data = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "times": {
                    prayer: time_obj.strftime("%H:%M")
                    for prayer, time_obj in prayer_times.items()
                },
            }
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f)
        except Exception as e:
            logging.warning(f"Cache save failed: {e}")

    def get_prayer_times(self) -> Optional[Dict[str, datetime]]:
        """Synchronously get times, trying cache then API."""
        cached = self._load_cached_times()
        if cached:
            logging.info("Using cached prayer times")
            return cached

        city = self.config.get("city")
        country = self.config.get("country")
        method = self.config.get("method")
        school = 1 if self.config.get("asr_jurisprudence") == "Hanafi" else 0

        for attempt in range(self.MAX_RETRIES):
            try:
                response = requests.get(
                    self.API_URL,
                    params={"city": city, "country": country, "method": method, "school": school},
                    timeout=10,
                )
                response.raise_for_status()
                data = response.json()["data"]["timings"]

                now = datetime.now()
                prayer_times = {}
                for prayer in ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]:
                    raw = data[prayer]
                    clean = self._clean_time_string(raw)
                    t = datetime.strptime(clean, "%H:%M").time()
                    prayer_times[prayer] = datetime.combine(now.date(), t)

                self._save_cached_times(prayer_times)
                logging.info(f"Fetched prayer times for {city}, {country}: {prayer_times}")
                return prayer_times
            except Exception as e:
                logging.warning(f"API attempt {attempt + 1} failed: {e}")

        # Final fallback: try cache even if date doesn't match (stale data better than nothing)
        try:
            if self.cache_file.exists():
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)
                today = datetime.now().date()
                return {
                    prayer: datetime.combine(today, datetime.strptime(time_str, "%H:%M").time())
                    for prayer, time_str in cache_data["times"].items()
                }
        except Exception:
            pass

        return None
