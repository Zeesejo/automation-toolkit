"""System Monitor: displays CPU, RAM, and Disk usage using psutil."""
import psutil
from rich.table import Table
from rich.console import Console

console = Console()

def show_system_stats():
    table = Table(title="System Stats", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan", width=20)
    table.add_column("Value", style="green")

    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    table.add_row("CPU Usage", f"{cpu}%")
    table.add_row("RAM Used", f"{ram.used / (1024**3):.2f} GB / {ram.total / (1024**3):.2f} GB ({ram.percent}%)")
    table.add_row("Disk Used", f"{disk.used / (1024**3):.2f} GB / {disk.total / (1024**3):.2f} GB ({disk.percent}%)")

    console.print(table)
