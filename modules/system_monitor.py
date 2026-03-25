"""System Monitor: displays CPU, RAM, Disk usage with alerts and CSV logging."""
import psutil
import csv
import os
from datetime import datetime
from rich.table import Table
from rich.console import Console
from config import THRESHOLDS, STATS_LOG_FILE

console = Console()

def show_system_stats(log: bool = True):
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    table = Table(title="System Stats", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", width=22)
    table.add_column("Value", style="green")
    table.add_column("Status", style="white")

    cpu_status  = "[bold red]⚠ HIGH[/bold red]" if cpu  >= THRESHOLDS["cpu_warn"]  else "[green]OK[/green]"
    ram_status  = "[bold red]⚠ HIGH[/bold red]" if ram.percent >= THRESHOLDS["ram_warn"]  else "[green]OK[/green]"
    disk_status = "[bold red]⚠ HIGH[/bold red]" if disk.percent >= THRESHOLDS["disk_warn"] else "[green]OK[/green]"

    table.add_row("CPU Usage",  f"{cpu}%", cpu_status)
    table.add_row("RAM Used",   f"{ram.used/(1024**3):.2f} GB / {ram.total/(1024**3):.2f} GB ({ram.percent}%)",  ram_status)
    table.add_row("Disk Used",  f"{disk.used/(1024**3):.2f} GB / {disk.total/(1024**3):.2f} GB ({disk.percent}%)", disk_status)
    console.print(table)

    if log:
        _log_to_csv(cpu, ram.percent, disk.percent)

def _log_to_csv(cpu, ram_pct, disk_pct):
    file_exists = os.path.isfile(STATS_LOG_FILE)
    with open(STATS_LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "cpu_pct", "ram_pct", "disk_pct"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), cpu, ram_pct, disk_pct])
    console.print(f"[dim]  → Stats logged to {STATS_LOG_FILE}[/dim]")
