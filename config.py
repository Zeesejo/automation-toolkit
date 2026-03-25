"""Central config for the Automation Toolkit."""

# --- Alert thresholds (%) ---
THRESHOLDS = {
    "cpu_warn":  80,   # warn if CPU  >= 80%
    "ram_warn":  85,   # warn if RAM  >= 85%
    "disk_warn": 90,   # warn if Disk >= 90%
}

# --- File Organizer ---
INBOX_FOLDER = "./inbox"

# --- Stats Logger ---
STATS_LOG_FILE = "./logs/system_stats.csv"

# --- Scheduler intervals ---
HEARTBEAT_SECONDS = 10
REMINDER_MINUTES  = 1
