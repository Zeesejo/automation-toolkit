"""Central config for the Automation Toolkit."""

# --- Alert thresholds (%) ---
THRESHOLDS = {
    "cpu_warn":  80,
    "ram_warn":  85,
    "disk_warn": 90,
}

# --- File Organizer ---
INBOX_FOLDER = "./inbox"

# --- Stats Logger ---
STATS_LOG_FILE = "./logs/system_stats.csv"

# --- Scheduler intervals ---
HEARTBEAT_SECONDS = 10
REMINDER_MINUTES  = 1

# --- Backup ---
BACKUP_SOURCES = [
    # Add paths to back up, e.g.:
    # r"C:\Users\zeese\Documents\Projects",
    # r"C:\Users\zeese\Desktop\important.txt",
]
BACKUP_DEST    = r".\backups"
BACKUP_KEEP    = 5   # max backups to keep per source
