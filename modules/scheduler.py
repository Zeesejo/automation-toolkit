"""Task Scheduler: runs jobs at defined intervals using the 'schedule' library."""
import schedule
import time
from rich.console import Console
from datetime import datetime

console = Console()

def job_heartbeat():
    console.print(f"  [dim][{datetime.now().strftime('%H:%M:%S')}] ♥ Heartbeat — scheduler is running...[/dim]")

def job_reminder():
    console.print(f"  [bold yellow][{datetime.now().strftime('%H:%M:%S')}] 🔔 Reminder: Check your task list![/bold yellow]")

def start_scheduler():
    # Heartbeat every 10 seconds
    schedule.every(10).seconds.do(job_heartbeat)
    # Reminder every 1 minute
    schedule.every(1).minutes.do(job_reminder)

    console.print("[green]Scheduler started. Heartbeat every 10s, reminder every 1min.[/green]")
    console.print("[dim]Press Ctrl+C to stop.[/dim]\n")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[bold red]Scheduler stopped.[/bold red]")
