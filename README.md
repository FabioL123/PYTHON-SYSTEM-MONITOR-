Original path: python-system-monitor/README.md
Note: this PDF displays the file's text. It is not a runnable replacement for the original .py, .sql, .yml, or configuration file.
# Python System Monitor
A command-line system monitoring tool that records CPU, RAM, and disk utilization plus host metadata. It
can print a snapshot and export it to JSON or CSV, with configurable warning thresholds.
## Requirements
- Python 3.10+
## Setup
```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
## Run
```bash
python monitor.py
python monitor.py --format json --output reports/system_snapshot.json
python monitor.py --format csv --output reports/system_snapshot.csv --cpu-limit 80 --memory-limit 85 --
disk-limit 90
```
## What it demonstrates
- Python CLI design and argument validation
- System metrics collection with `psutil`
- JSON/CSV reporting and filesystem handling
- Threshold-based warnings
## Notes
This records a point-in-time snapshot, not a long-running monitoring agent. Disk usage is measured for
the root filesystem. Review permissions and platform behavior before extending it.
