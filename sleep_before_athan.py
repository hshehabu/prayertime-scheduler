import requests
import time
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
import sys
import json
from pathlib import Path
import platform

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

CONFIG = {
    "CITY": "Addis Ababa",
    "COUNTRY": "Ethiopia",
    "METHOD": 3, # Muslim World League
    "ALERT_MINUTES_BEFORE": 5,
    "API_URL": "https://api.aladhan.com/v1/timingsByCity",
    "MAX_RETRIES": 3,
    "CACHE_FILE": "prayer_times_cache.json"
}

def load_cached_prayer_times() -> Optional[Dict[str, datetime]]:
    """Load prayer times from cache if available and valid for today."""
    try:
        if not Path(CONFIG["CACHE_FILE"]).exists():
            return None
            
        with open(CONFIG["CACHE_FILE"], 'r') as f:
            cache_data = json.load(f)
            
        cached_date = datetime.strptime(cache_data['date'], '%Y-%m-%d').date()
        if cached_date != datetime.now().date():
            return None
            
        return {
            prayer: datetime.strptime(time_str, '%H:%M')
            for prayer, time_str in cache_data['times'].items()
        }
    except Exception as e:
        logging.warning(f"Failed to load cache: {e}")
        return None

def save_prayer_times_to_cache(prayer_times: Dict[str, datetime]) -> None:
    """Save prayer times to cache file."""
    try:
        cache_data = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'times': {
                prayer: time_obj.strftime('%H:%M')
                for prayer, time_obj in prayer_times.items()
            }
        }
        with open(CONFIG["CACHE_FILE"], 'w') as f:
            json.dump(cache_data, f)
    except Exception as e:
        logging.warning(f"Failed to save cache: {e}")

def get_prayer_times() -> dict[str, datetime] | None:
    """
    Fetch prayer times from the API with retry mechanism.
    Returns a dictionary of prayer names to datetime objects.
    Uses cache if available and valid for today.
    """
    cached_times = load_cached_prayer_times()
    if cached_times:
        logging.info("Using cached prayer times")
        return cached_times

    for attempt in range(CONFIG["MAX_RETRIES"]):
        try:
            response = requests.get(
                CONFIG["API_URL"],
                params={
                    "city": CONFIG["CITY"],
                    "country": CONFIG["COUNTRY"],
                    "method": CONFIG["METHOD"],
                },
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()["data"]["timings"]
            prayer_times = {
                prayer: datetime.strptime(data[prayer], "%H:%M")
                for prayer in ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
            }
            
            # Save to cache
            save_prayer_times_to_cache(prayer_times)
            return prayer_times
            
        except (requests.RequestException, KeyError, ValueError) as e:
            if attempt < CONFIG["MAX_RETRIES"] - 1:
                wait_time = (2 ** attempt) * 1  # Exponential backoff
                logging.warning(f"API request failed (attempt {attempt + 1}/{CONFIG['MAX_RETRIES']}): {e}")
                logging.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logging.error(f"Failed to fetch prayer times after {CONFIG['MAX_RETRIES']} attempts: {e}")
                sys.exit(1)

def sleep_pc() -> None:
    """Put the PC to sleep using the appropriate command for the OS."""
    try:
        current_os = platform.system()
        if current_os == 'Windows':
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        elif current_os == 'Linux':
            os.system("sudo systemctl suspend")
        else:
            logging.error(f"Unsupported operating system: {current_os}")
            sys.exit(1)
    except Exception as e:
        logging.error(f"Failed to put PC to sleep: {e}")
        sys.exit(1)

def wait_and_sleep(prayer_times: Dict[str, datetime]) -> None:
    """
    Wait until 5 minutes before the next prayer time and then sleep the PC.
    """
    now = datetime.now()
    next_prayer_time: Optional[datetime] = None
    next_prayer_name: Optional[str] = None

    # Find the next prayer time
    for prayer, time_obj in prayer_times.items():
        alert_time = datetime.combine(now.date(), time_obj.time()) - timedelta(minutes=CONFIG["ALERT_MINUTES_BEFORE"])
        if alert_time > now:
            if next_prayer_time is None or alert_time < next_prayer_time:
                next_prayer_time = alert_time
                next_prayer_name = prayer

    if next_prayer_time is None:
        logging.info("No upcoming prayer times found for today")
        return

    wait_time = (next_prayer_time - now).total_seconds()
    hours = int(wait_time // 3600)
    minutes = int((wait_time % 3600) // 60)
    logging.info(f"Will sleep PC at {next_prayer_time.time()} (5 minutes before {next_prayer_name})")
    logging.info(f"Time remaining: {hours} hours and {minutes} minutes")
    
    try:
        time.sleep(wait_time)
        logging.info(f"Sleeping PC now for {next_prayer_name}...")
        sleep_pc()
    except KeyboardInterrupt:
        logging.info("Sleep operation cancelled by user")
        sys.exit(0)

def main():
    """Main function to run the prayer time sleep program."""
    try:
        prayer_times = get_prayer_times()
        wait_and_sleep(prayer_times)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


