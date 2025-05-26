# PrayerTime Scheduler

A Python utility that helps developers and PC users manage their work schedule around prayer times. The script automatically puts your PC to sleep 5 minutes before each prayer time, ensuring you don't miss your prayers while working.

## Features

- Automatically fetches prayer times for your location
- Puts PC to sleep 5 minutes before each prayer time
- Caches prayer times to reduce API calls
- Supports Windows operating system
- Configurable city and calculation method
- Built-in retry mechanism for API reliability

## Requirements

- Python 3.6+
- Windows operating system
- Internet connection (for initial prayer time fetch)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/prayer-time-scheduler.git
cd prayer-time-scheduler
```

2. Install required packages:
```bash
pip install requests
```

## Configuration

Edit the `CONFIG` dictionary in `sleep_before_athan.py` to customize:
- `CITY`: Your city name
- `COUNTRY`: Your country name
- `METHOD`: Prayer time calculation method (default: 3 - Muslim World League)
- `ALERT_MINUTES_BEFORE`: Minutes before prayer to put PC to sleep (default: 5)

## Usage

Simply run the script:
```bash
python sleep_before_athan.py
```

The script will:
1. Fetch prayer times for your location
2. Calculate the next prayer time
3. Put your PC to sleep 5 minutes before the prayer time
4. This gives you time to prepare for prayer without being distracted by work

## Notes

- The script uses the Aladhan API to fetch prayer times
- Prayer times are cached for the current day to minimize API calls
- You can cancel the sleep operation at any time using Ctrl+C
- Perfect for developers and professionals who want to maintain their prayer schedule while working

## License

MIT License 