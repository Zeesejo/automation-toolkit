"""File Organizer: sorts files in a target folder by extension."""
import os
import shutil
from pathlib import Path
from rich.console import Console

console = Console()

EXTENSION_MAP = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos":     [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
    "Documents":  [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Code":       [".py", ".js", ".ts", ".html", ".css", ".json", ".yaml", ".yml"],
    "Archives":   [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Audio":      [".mp3", ".wav", ".flac", ".aac"],
}

def organize_folder(folder_path: str):
    folder = Path(folder_path)
    if not folder.exists():
        folder.mkdir(parents=True)
        console.print(f"[yellow]Created folder:[/yellow] {folder.resolve()}")
        console.print("[dim]Drop files into the 'inbox' folder and re-run to organize them.[/dim]")
        return

    moved = 0
    for file in folder.iterdir():
        if file.is_file():
            category = "Others"
            for cat, exts in EXTENSION_MAP.items():
                if file.suffix.lower() in exts:
                    category = cat
                    break
            dest_dir = folder / category
            dest_dir.mkdir(exist_ok=True)
            shutil.move(str(file), str(dest_dir / file.name))
            console.print(f"  [green]Moved[/green] {file.name} → {category}/")
            moved += 1

    if moved == 0:
        console.print("[dim]No files to organize.[/dim]")
    else:
        console.print(f"[bold green]✔ Organized {moved} file(s).[/bold green]")
