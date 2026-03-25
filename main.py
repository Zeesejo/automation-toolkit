"""Automation Toolkit - Entry Point"""
import os
from modules.file_organizer import organize_folder
from modules.system_monitor import show_system_stats
from modules.scheduler import start_scheduler
from config import INBOX_FOLDER, STATS_LOG_FILE
from rich.console import Console
from rich.panel import Panel

console = Console()

def setup_dirs():
    """Ensure required folders exist."""
    os.makedirs(INBOX_FOLDER, exist_ok=True)
    os.makedirs(os.path.dirname(STATS_LOG_FILE), exist_ok=True)

def main():
    console.print(Panel.fit("[bold green]🤖 Automation Toolkit[/bold green]", subtitle="by Zeesejo"))
    setup_dirs()

    console.print("\n[bold cyan]── System Monitor ──[/bold cyan]")
    show_system_stats(log=True)

    console.print("\n[bold cyan]── File Organizer ──[/bold cyan]")
    organize_folder(INBOX_FOLDER)

    console.print("\n[bold cyan]── Scheduler (Ctrl+C to stop) ──[/bold cyan]")
    start_scheduler()

if __name__ == "__main__":
    main()
