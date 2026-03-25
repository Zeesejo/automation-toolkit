"""Task Scheduler: runs jobs at defined intervals."""
import schedule
import time
from rich.console import Console
from datetime import datetime
from config import HEARTBEAT_SECONDS, REMINDER_MINUTES
from modules.system_monitor import show_system_stats

console = Console()

def job_heartbeat():
    console.print(f"  [dim][{datetime.now().strftime('%H:%M:%S')}] ♥ Heartbeat — scheduler is alive[/dim]")

def job_reminder():
    console.print(f"  [bold yellow][{datetime.now().strftime('%H:%M:%S')}] 🔔 Reminder: Check your task list![/bold yellow]")

def job_log_stats():
    console.print(f"\n  [bold cyan][{datetime.now().strftime('%H:%M:%S')}] 📊 Logging system stats...[/bold cyan]")
    show_system_stats(log=True)

def start_scheduler():
    schedule.every(HEARTBEAT_SECONDS).seconds.do(job_heartbeat)
    schedule.every(REMINDER_MINUTES).minutes.do(job_reminder)
    schedule.every(5).minutes.do(job_log_stats)   # auto-log stats every 5 min

    console.print(f"[green]Scheduler started.[/green] Heartbeat every {HEARTBEAT_SECONDS}s | Reminder every {REMINDER_MINUTES}min | Stats logged every 5min")
    console.print("[dim]Press Ctrl+C to stop.\n[/dim]")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[bold red]Scheduler stopped.[/bold red]")
