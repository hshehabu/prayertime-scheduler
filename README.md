# 🕌 PrayerTime Scheduler

[![Python Version](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Windows](https://img.shields.io/badge/Windows-Supported-green.svg)](https://www.microsoft.com/windows)

A Python utility that helps developers and PC users manage their work schedule around prayer times. The script automatically puts your PC to sleep 5 minutes before each prayer time, ensuring you don't miss your prayers while working.

## ✨ Features

- ⏰ Automatically fetches prayer times for your location
- 💤 Puts PC to sleep 5 minutes before each prayer time
- 💾 Caches prayer times to reduce API calls
- 🪟 Supports Windows operating system
- ⚙️ Configurable city and calculation method
- 🔄 Built-in retry mechanism for API reliability

## 📋 Requirements

- 🐍 Python 3.6+
- 🪟 Windows operating system
- 🌐 Internet connection (for initial prayer time fetch)

## 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/prayer-time-scheduler.git
cd prayer-time-scheduler
```






## ⚙️ Configuration

Edit the `CONFIG` dictionary in `sleep_before_athan.py` to customize:
- 🏙️ `CITY`: Your city name
- 🌍 `COUNTRY`: Your country name
- 📏 `METHOD`: Prayer time calculation method (default: 3 - Muslim World League)
- ⏱️ `ALERT_MINUTES_BEFORE`: Minutes before prayer to put PC to sleep (default: 5)

## 💻 Usage

Simply run the script:
```bash
python sleep_before_athan.py
```

The script will:
1. 📡 Fetch prayer times for your location
2. ⏰ Calculate the next prayer time
3. 💤 Put your PC to sleep 5 minutes before the prayer time
4. 🧘 This gives you time to prepare for prayer without being distracted by work

## 📝 Notes

- 🔌 The script uses the Aladhan API to fetch prayer times
- 💾 Prayer times are cached for the current day to minimize API calls
- ⌨️ You can cancel the sleep operation at any time using Ctrl+C
- 👨‍💻 Perfect for developers and professionals who want to maintain their prayer schedule while working

## 🤝 Contributing

This project is open source and we welcome contributions from the community! Whether you want to report a bug, suggest a feature, or submit a pull request, your help is appreciated.

### How to Contribute

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Contribution Guidelines

- Please ensure your code follows the existing style and formatting
- Add comments to explain complex logic
- Write clear commit messages
- Update documentation if you add new features
- Test your changes thoroughly

## 📄 License

MIT License 
