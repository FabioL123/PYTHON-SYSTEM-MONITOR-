Original path: python-system-monitor/monitor.py
Note: this PDF displays the file's text. It is not a runnable replacement for the original .py, .sql, .yml, or configuration file.
#!/usr/bin/env python3
"""Collect basic system metrics and optionally export them to JSON or CSV."""
from __future__ import annotations
import argparse
import csv
import json
import os
import platform
import shutil
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
try:
 import psutil
except ImportError as exc: # Friendly error for users who forgot dependencies.
 raise SystemExit("Missing dependency 'psutil'. Install with: python -m pip install -r requirements.
txt") from exc
def collect_metrics() -> dict[str, Any]:
 """Return a snapshot of CPU, memory, disk, and host metadata."""
 disk_path = os.path.abspath(os.sep)
 disk = shutil.disk_usage(disk_path)
 memory = psutil.virtual_memory()
 return {
 "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
 "hostname": platform.node() or "unknown",
 "platform": platform.platform(),
 "cpu_percent": psutil.cpu_percent(interval=0.2),
 "memory_percent": memory.percent,
 "memory_total_bytes": memory.total,
 "memory_available_bytes": memory.available,
 "disk_percent": round((disk.used / disk.total) * 100, 2) if disk.total else 0.0,
 "disk_total_bytes": disk.total,
 "disk_free_bytes": disk.free,
 }
def get_warnings(metrics: dict[str, Any], cpu_limit: float, memory_limit: float, disk_limit: float) ->
list[str]:
 warnings = []
 for metric, limit in (("cpu_percent", cpu_limit), ("memory_percent", memory_limit), ("disk_percent",
disk_limit)):
 value = float(metrics[metric])
 if value >= limit:
 warnings.append(f"{metric} is {value:.1f}% (threshold: {limit:.1f}%)")
 return warnings
def export_metrics(metrics: dict[str, Any], output: Path, fmt: str) -> None:
 output.parent.mkdir(parents=True, exist_ok=True)
 if fmt == "json":
 output.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
 else:
 with output.open("w", newline="", encoding="utf-8") as handle:
 writer = csv.DictWriter(handle, fieldnames=list(metrics.keys()))
 writer.writeheader()
 writer.writerow(metrics)
def main() -> int:
 parser = argparse.ArgumentParser(description=__doc__)
 parser.add_argument("--format", choices=("json", "csv"), default="json", help="export format (
default: json)")
 parser.add_argument("--output", type=Path, help="optional output file path")
 parser.add_argument("--cpu-limit", type=float, default=90.0, help="CPU warning threshold percent")
 parser.add_argument("--memory-limit", type=float, default=90.0, help="memory warning threshold
percent")
 parser.add_argument("--disk-limit", type=float, default=90.0, help="disk warning threshold percent")
 args = parser.parse_args()
 for name in ("cpu_limit", "memory_limit", "disk_limit"):
 value = getattr(args, name)
 if not 0 <= value <= 100:
 parser.error(f"--{name.replace('_', '-')} must be between 0 and 100")
 metrics = collect_metrics()
 print(json.dumps(metrics, indent=2))
 warnings = get_warnings(metrics, args.cpu_limit, args.memory_limit, args.disk_limit)
 if warnings:
 print("\nWARNINGS:")
 for warning in warnings:
 print(f"- {warning}")
 if args.output:
 export_metrics(metrics, args.output, args.format)
 print(f"\nSaved {args.format.upper()} report to {args.output}")
 return 0
if __name__ == "__main__":
 raise SystemExit(main())
