"""Interactive CLI Menu for Automation Toolkit."""
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box
import sys

console = Console()

MENU_OPTIONS = [
    ("1", "System Monitor",      "Show CPU, RAM, Disk stats (+ log to CSV)"),
    ("2", "File Organizer",      "Sort files in ./inbox by type"),
    ("3", "Start Scheduler",     "Run background heartbeat + reminder jobs"),
    ("4", "View Stats Log",      "Print last 10 rows from logs/system_stats.csv"),
    ("5", "Stats Dashboard",     "Plot CPU/RAM/Disk history as a chart"),
    ("6", "Edit Config",         "Change alert thresholds & intervals"),
    ("0", "Exit",                "Quit the toolkit"),
]

def print_menu():
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("#",       style="bold cyan",  width=4)
    table.add_column("Module",  style="bold white", width=20)
    table.add_column("Description", style="dim")
    for key, name, desc in MENU_OPTIONS:
        table.add_row(key, name, desc)
    console.print(table)

def run_menu():
    console.print(Panel.fit("[bold green]\U0001f916 Automation Toolkit[/bold green]", subtitle="Interactive Mode"))

    while True:
        console.print()
        print_menu()
        choice = Prompt.ask("\n[bold cyan]Select an option[/bold cyan]", choices=[o[0] for o in MENU_OPTIONS], default="1")

        if choice == "1":
            from modules.system_monitor import show_system_stats
            console.print("\n[bold cyan]\u2500\u2500 System Monitor \u2500\u2500[/bold cyan]")
            show_system_stats(log=True)

        elif choice == "2":
            from modules.file_organizer import organize_folder
            from config import INBOX_FOLDER
            console.print("\n[bold cyan]\u2500\u2500 File Organizer \u2500\u2500[/bold cyan]")
            organize_folder(INBOX_FOLDER)

        elif choice == "3":
            from modules.scheduler import start_scheduler
            console.print("\n[bold cyan]\u2500\u2500 Scheduler (Ctrl+C to return to menu) \u2500\u2500[/bold cyan]")
            start_scheduler()

        elif choice == "4":
            _view_stats_log()

        elif choice == "5":
            from modules.dashboard import show_dashboard
            console.print("\n[bold cyan]\u2500\u2500 Stats Dashboard \u2500\u2500[/bold cyan]")
            show_dashboard()

        elif choice == "6":
            _edit_config()

        elif choice == "0":
            if Confirm.ask("[red]Are you sure you want to exit?[/red]"):
                console.print("[bold green]Goodbye! \U0001f44b[/bold green]")
                sys.exit(0)

def _view_stats_log():
    import csv, os
    from config import STATS_LOG_FILE
    console.print("\n[bold cyan]\u2500\u2500 Stats Log (last 10 entries) \u2500\u2500[/bold cyan]")
    if not os.path.isfile(STATS_LOG_FILE):
        console.print("[yellow]No log file found yet. Run System Monitor first.[/yellow]")
        return
    with open(STATS_LOG_FILE, newline="") as f:
        rows = list(csv.reader(f))
    if len(rows) <= 1:
        console.print("[yellow]Log is empty.[/yellow]")
        return
    headers = rows[0]
    data    = [r for r in rows[1:] if r != headers][-10:]
    table = Table(box=box.SIMPLE, show_header=True, header_style="bold magenta")
    for h in headers:
        table.add_column(h, style="cyan")
    for row in data:
        styled = list(row)
        try:
            if float(row[2]) >= 85:
                styled[2] = f"[bold red]{row[2]}[/bold red]"
        except (IndexError, ValueError):
            pass
        table.add_row(*styled)
    console.print(table)

def _edit_config():
    import config
    console.print("\n[bold cyan]\u2500\u2500 Edit Config \u2500\u2500[/bold cyan]")
    console.print(f"Current: cpu_warn=[yellow]{config.THRESHOLDS['cpu_warn']}%[/yellow]  ram_warn=[yellow]{config.THRESHOLDS['ram_warn']}%[/yellow]  disk_warn=[yellow]{config.THRESHOLDS['disk_warn']}%[/yellow]")

    def ask_int(prompt, default):
        while True:
            val = Prompt.ask(prompt, default=str(default))
            try:
                return int(val)
            except ValueError:
                console.print(f"[red]Please enter a number, got: '{val}'[/red]")

    cpu  = ask_int("New CPU  warn threshold (%)",  config.THRESHOLDS["cpu_warn"])
    ram  = ask_int("New RAM  warn threshold (%)",  config.THRESHOLDS["ram_warn"])
    disk = ask_int("New Disk warn threshold (%)", config.THRESHOLDS["disk_warn"])
    hb   = ask_int("Heartbeat interval (seconds)", config.HEARTBEAT_SECONDS)
    rm   = ask_int("Reminder interval (minutes)",  config.REMINDER_MINUTES)

    new_config = f'''"""Central config for the Automation Toolkit."""

# --- Alert thresholds (%) ---
THRESHOLDS = {{
    "cpu_warn":  {cpu},
    "ram_warn":  {ram},
    "disk_warn": {disk},
}}

# --- File Organizer ---
INBOX_FOLDER = "./inbox"

# --- Stats Logger ---
STATS_LOG_FILE = "./logs/system_stats.csv"

# --- Scheduler intervals ---
HEARTBEAT_SECONDS = {hb}
REMINDER_MINUTES  = {rm}
'''
    with open("config.py", "w") as f:
        f.write(new_config)
    console.print("[bold green]\u2714 Config saved! Restart the toolkit for scheduler changes to take effect.[/bold green]")
