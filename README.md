<div align="center">

# Automation Toolkit

**A modular Python automation suite for system monitoring, file organization, smart scheduling, and auto-backup — built and maintained by [Litends](https://litends.com)**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Zeesejo/automation-toolkit?style=social)](https://github.com/Zeesejo/automation-toolkit/stargazers)
[![Made by Litends](https://img.shields.io/badge/Made%20by-Litends-blueviolet)](https://litends.com)

</div>

---

## What is this?

Automation Toolkit is a **production-ready, zero-dependency-config** Python toolkit that runs on your local machine and automates the boring stuff:

| Module | What it does |
|---|---|
| System Monitor | Real-time CPU, RAM & Disk stats with threshold alerts |
| File Organizer | Auto-sorts your `inbox/` folder by file type |
| Task Scheduler | Background heartbeat, reminders & stat logging |
| Stats Dashboard | Dark-themed matplotlib chart from your collected CSV data |
| Auto Backup | Zips folders to timestamped archives, auto-prunes old ones |
| Desktop Alerts | Windows toast notifications when thresholds are breached |
| Interactive CLI | Rich-powered menu — no command memorization needed |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/Zeesejo/automation-toolkit.git
cd automation-toolkit

# 2. Create & activate virtual environment (Windows)
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python main.py
```

> **VS Code users:** Open the folder, select `.venv` as your Python interpreter, then press **F5** to run directly.

---

## Project Structure

```
automation-toolkit/
├── main.py                   # Entry point
├── menu.py                   # Interactive CLI menu
├── config.py                 # Central config (thresholds, paths, intervals)
├── requirements.txt
├── modules/
│   ├── system_monitor.py     # CPU/RAM/Disk stats + CSV logging
│   ├── file_organizer.py     # File sorting by extension
│   ├── scheduler.py          # Background job scheduler
│   ├── dashboard.py          # Matplotlib stats chart
│   ├── backup.py             # Zip-based auto-backup engine
│   └── notifier.py           # Windows desktop notifications
├── logs/                     # system_stats.csv + dashboard.png
├── inbox/                    # Drop files here to auto-organize
└── backups/                  # Timestamped zip archives
```

---

## Configuration

Edit `config.py` to customize everything — or use **menu option 7 (Edit Config)** at runtime:

```python
THRESHOLDS = {
    "cpu_warn":  80,   # Alert when CPU  >= 80%
    "ram_warn":  85,   # Alert when RAM  >= 85%
    "disk_warn": 90,   # Alert when Disk >= 90%
}

HEARTBEAT_SECONDS = 10   # Scheduler heartbeat interval
REMINDER_MINUTES  = 1    # Reminder job interval

BACKUP_SOURCES = [
    r"C:\Users\YourName\Documents",
]
BACKUP_DEST = r".\backups"
BACKUP_KEEP = 5           # Max zip archives to keep per source
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `psutil` | System stats (CPU, RAM, Disk) |
| `rich` | Beautiful terminal UI |
| `schedule` | Job scheduling |
| `matplotlib` | Stats chart rendering |
| `plyer` | Cross-platform desktop notifications |

---

## Built by Litends

This project is part of the open-source tooling maintained by **[Litends](https://litends.com)** — building robust intelligent systems.

- Website: [litends.com](https://litends.com)
- GitHub: [@Zeesejo](https://github.com/Zeesejo)
- Author: **Zeeshan Modi** — AI/ML Engineer, M.Sc. AIIS @ University of Bremen

---

## License

MIT License — free to use, modify, and distribute.
