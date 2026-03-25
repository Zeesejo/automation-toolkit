"""Auto-backup: zips source folders and saves timestamped archives."""
import os
import zipfile
import shutil
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box
from config import BACKUP_SOURCES, BACKUP_DEST, BACKUP_KEEP

console = Console()

def _zip_folder(src: Path, dest_dir: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name  = f"{src.name}_{timestamp}.zip"
    zip_path  = dest_dir / zip_name
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        if src.is_file():
            zf.write(src, src.name)
        else:
            for file in src.rglob("*"):
                if file.is_file():
                    zf.write(file, file.relative_to(src.parent))
    return zip_path

def _prune_old_backups(dest_dir: Path, src_name: str):
    """Keep only the N most recent backups for a given source."""
    existing = sorted(dest_dir.glob(f"{src_name}_*.zip"), key=os.path.getmtime)
    while len(existing) > BACKUP_KEEP:
        oldest = existing.pop(0)
        oldest.unlink()
        console.print(f"  [dim]Pruned old backup: {oldest.name}[/dim]")

def run_backup(sources=None):
    dest = Path(BACKUP_DEST)
    dest.mkdir(parents=True, exist_ok=True)

    targets = sources or BACKUP_SOURCES
    if not targets:
        console.print("[yellow]No backup sources configured. Edit BACKUP_SOURCES in config.py[/yellow]")
        return

    total_size = 0
    backed_up  = []

    for src_str in targets:
        src = Path(src_str)
        if not src.exists():
            console.print(f"  [yellow]Skipping (not found): {src}[/yellow]")
            continue
        console.print(f"  [cyan]Backing up:[/cyan] {src} ...")
        zip_path = _zip_folder(src, dest)
        size_kb  = zip_path.stat().st_size / 1024
        total_size += size_kb
        backed_up.append((src.name, zip_path.name, f"{size_kb:.1f} KB"))
        _prune_old_backups(dest, src.name)

    if backed_up:
        table = Table(box=box.SIMPLE, show_header=True, header_style="bold magenta")
        table.add_column("Source",   style="cyan")
        table.add_column("Archive",  style="white")
        table.add_column("Size",     style="green")
        for row in backed_up:
            table.add_row(*row)
        console.print(table)
        console.print(f"[bold green]  Backup complete! {len(backed_up)} archive(s), {total_size:.1f} KB total -> {dest.resolve()}[/bold green]")
    else:
        console.print("[yellow]Nothing was backed up.[/yellow]")

def show_backups():
    dest = Path(BACKUP_DEST)
    if not dest.exists():
        console.print("[yellow]No backups directory yet.[/yellow]")
        return
    archives = sorted(dest.glob("*.zip"), key=os.path.getmtime, reverse=True)
    if not archives:
        console.print("[yellow]No backup archives found.[/yellow]")
        return
    table = Table(title=f"Backups in {dest}", box=box.ROUNDED, header_style="bold magenta")
    table.add_column("Archive",  style="cyan")
    table.add_column("Size",     style="green")
    table.add_column("Modified", style="white")
    for a in archives:
        mtime = datetime.fromtimestamp(a.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        size  = f"{a.stat().st_size/1024:.1f} KB"
        table.add_row(a.name, size, mtime)
    console.print(table)

def add_source_interactive():
    path = Prompt.ask("Enter the full path to the folder/file you want to back up")
    src  = Path(path.strip())
    if not src.exists():
        console.print(f"[red]Path does not exist: {src}[/red]")
        return
    # Append to config
    import config
    if path not in config.BACKUP_SOURCES:
        config.BACKUP_SOURCES.append(path)
        _rewrite_config(config)
        console.print(f"[green]Added '{src}' to backup sources.[/green]")
    else:
        console.print("[yellow]Already in backup sources.[/yellow]")

def _rewrite_config(config):
    sources_repr = "[\n"
    for s in config.BACKUP_SOURCES:
        sources_repr += f'    r"{s}",\n'
    sources_repr += "]"
    content = f'''"""Central config for the Automation Toolkit."""

# --- Alert thresholds (%) ---
THRESHOLDS = {{
    "cpu_warn":  {config.THRESHOLDS["cpu_warn"]},
    "ram_warn":  {config.THRESHOLDS["ram_warn"]},
    "disk_warn": {config.THRESHOLDS["disk_warn"]},
}}

# --- File Organizer ---
INBOX_FOLDER = "./inbox"

# --- Stats Logger ---
STATS_LOG_FILE = "./logs/system_stats.csv"

# --- Scheduler intervals ---
HEARTBEAT_SECONDS = {config.HEARTBEAT_SECONDS}
REMINDER_MINUTES  = {config.REMINDER_MINUTES}

# --- Backup ---
BACKUP_SOURCES = {sources_repr}
BACKUP_DEST    = r"{config.BACKUP_DEST}"
BACKUP_KEEP    = {config.BACKUP_KEEP}   # max backups to keep per source
'''
    with open("config.py", "w") as f:
        f.write(content)
