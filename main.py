"""Automation Toolkit - Entry Point"""
import os
from config import INBOX_FOLDER, STATS_LOG_FILE

def setup_dirs():
    os.makedirs(INBOX_FOLDER, exist_ok=True)
    os.makedirs(os.path.dirname(STATS_LOG_FILE), exist_ok=True)

def main():
    setup_dirs()
    from menu import run_menu
    run_menu()

if __name__ == "__main__":
    main()
