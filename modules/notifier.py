"""Desktop Notifier: sends Windows toast notifications for system alerts."""
from rich.console import Console

console = Console()

def _toast(title: str, message: str, icon: str = "warning"):
    """Send a Windows toast notification using plyer."""
    try:
        from plyer import notification
        notification.notify(
            title=title,
            message=message,
            app_name="Automation Toolkit",
            app_icon=None,
            timeout=8,
        )
    except Exception as e:
        console.print(f"[dim red]Notification failed: {e}[/dim red]")

def check_and_notify(cpu: float, ram_pct: float, disk_pct: float):
    """Compare metrics against thresholds and fire notifications if exceeded."""
    from config import THRESHOLDS
    alerts = []

    if cpu >= THRESHOLDS["cpu_warn"]:
        msg = f"CPU usage is at {cpu}% (threshold: {THRESHOLDS['cpu_warn']}%)"
        alerts.append(("⚠ CPU Alert", msg))
        console.print(f"[bold red]  ⚠ CPU ALERT: {msg}[/bold red]")

    if ram_pct >= THRESHOLDS["ram_warn"]:
        msg = f"RAM usage is at {ram_pct}% (threshold: {THRESHOLDS['ram_warn']}%)"
        alerts.append(("⚠ RAM Alert", msg))
        console.print(f"[bold red]  ⚠ RAM ALERT: {msg}[/bold red]")

    if disk_pct >= THRESHOLDS["disk_warn"]:
        msg = f"Disk usage is at {disk_pct}% (threshold: {THRESHOLDS['disk_warn']}%)"
        alerts.append(("⚠ Disk Alert", msg))
        console.print(f"[bold red]  ⚠ DISK ALERT: {msg}[/bold red]")

    for title, message in alerts:
        _toast(title, message)

    if not alerts:
        console.print("[dim green]  ✔ All metrics within normal range.[/dim green]")
