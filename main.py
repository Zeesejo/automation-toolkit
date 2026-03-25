"""Automation Toolkit - Entry Point"""
from modules.file_organizer import organize_folder
from modules.system_monitor import show_system_stats
from modules.scheduler import start_scheduler
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    console.print(Panel.fit("[bold green]🤖 Automation Toolkit[/bold green]", subtitle="by Zeesejo"))

    # 1. Show current system stats
    console.print("\n[bold cyan]── System Monitor ──[/bold cyan]")
    show_system_stats()

    # 2. Organize the ./inbox folder
    console.print("\n[bold cyan]── File Organizer ──[/bold cyan]")
    organize_folder("./inbox")

    # 3. Start the background scheduler
    console.print("\n[bold cyan]── Scheduler (press Ctrl+C to stop) ──[/bold cyan]")
    start_scheduler()

if __name__ == "__main__":
    main()
