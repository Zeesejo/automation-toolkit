# 🤖 Automation Toolkit

A ready-to-run Python automation toolkit for your local machine.

## Features
- **File Organizer** – Auto-sorts files in a folder by extension
- **Task Scheduler** – Runs jobs at defined intervals
- **System Monitor** – Logs CPU, RAM, and disk usage

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/Zeesejo/automation-toolkit.git
cd automation-toolkit

# 2. Create a virtual environment
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On Linux/Mac
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Run

```bash
# Run the full automation suite
python main.py

# Or run modules individually
python modules/file_organizer.py
python modules/system_monitor.py
python modules/scheduler.py
```

## VS Code
Open the folder in VS Code, select the `.venv` Python interpreter, and press **F5** or use the Run button.
