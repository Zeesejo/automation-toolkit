"""Stats Dashboard: plots CPU, RAM, Disk history from the CSV log."""
import os
import csv
from datetime import datetime
from rich.console import Console

console = Console()

def show_dashboard():
    from config import STATS_LOG_FILE

    if not os.path.isfile(STATS_LOG_FILE):
        console.print("[yellow]No stats log found. Run System Monitor first to collect data.[/yellow]")
        return

    timestamps, cpu_vals, ram_vals, disk_vals = [], [], [], []

    with open(STATS_LOG_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                timestamps.append(datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S"))
                cpu_vals.append(float(row["cpu_pct"]))
                ram_vals.append(float(row["ram_pct"]))
                disk_vals.append(float(row["disk_pct"]))
            except (ValueError, KeyError):
                continue

    if len(timestamps) < 2:
        console.print("[yellow]Not enough data points yet (need at least 2). Keep the scheduler running to collect more.[/yellow]")
        return

    try:
        import matplotlib
        matplotlib.use("TkAgg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        console.print("[red]matplotlib not installed. Run: pip install matplotlib[/red]")
        return

    from config import THRESHOLDS

    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=True)
    # ASCII-safe title (no emoji to avoid font warning)
    fig.suptitle("Automation Toolkit -- System Stats Dashboard", fontsize=14, fontweight="bold", color="white")
    fig.patch.set_facecolor("#1e1e2e")

    datasets = [
        (axes[0], cpu_vals,  "CPU %",  "#74c7ec", THRESHOLDS["cpu_warn"]),
        (axes[1], ram_vals,  "RAM %",  "#f38ba8", THRESHOLDS["ram_warn"]),
        (axes[2], disk_vals, "Disk %", "#a6e3a1", THRESHOLDS["disk_warn"]),
    ]

    for ax, values, label, color, threshold in datasets:
        ax.set_facecolor("#181825")
        ax.plot(timestamps, values, color=color, linewidth=2, marker="o", markersize=4, label=label)
        ax.fill_between(timestamps, values, alpha=0.15, color=color)
        ax.axhline(y=threshold, color="#f9e2af", linestyle="--", linewidth=1, label=f"Threshold ({threshold}%)")
        ax.set_ylim(0, 105)
        ax.set_ylabel(label, color="white", fontsize=10)
        ax.tick_params(colors="white")
        ax.spines[:].set_color("#45475a")
        ax.legend(loc="upper right", fontsize=8, facecolor="#313244", labelcolor="white")
        ax.yaxis.grid(True, color="#45475a", linestyle=":")

    axes[2].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    axes[2].xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=30, color="white")
    plt.tight_layout()

    out_path = "./logs/dashboard.png"
    plt.savefig(out_path, dpi=120, bbox_inches="tight", facecolor=fig.get_facecolor())
    console.print(f"[dim]  -> Chart saved to {out_path}[/dim]")
    console.print("[green]Opening dashboard chart...[/green]")
    plt.show()
