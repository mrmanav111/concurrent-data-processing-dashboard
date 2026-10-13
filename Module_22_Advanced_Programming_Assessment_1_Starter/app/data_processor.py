from __future__ import annotations

import csv
import time
from pathlib import Path


def load_records(folder: str | Path) -> list[dict]:
    """Load all CSV records from the supplied folder."""
    folder = Path(folder)
    records: list[dict] = []

    for csv_file in sorted(folder.glob("*.csv")):
        with csv_file.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                row["source_file"] = csv_file.name
                row["value"] = float(row["value"])
                records.append(row)

    return records


def process_records(records: list[dict], progress_callback=None) -> dict:
    """
    Process records and return a summary.

    This function deliberately performs work slowly so that calling it directly
    from a GUI event handler makes the interface unresponsive. Students are
    expected to move this processing to a suitable background worker/thread/task.
    """
    if not records:
        raise ValueError("No records were supplied for processing.")

    totals: dict[str, float] = {}
    count = len(records)

    for index, record in enumerate(records, start=1):
        time.sleep(0.12)  # deliberate delay to simulate longer-running work
        category = record["category"]
        totals[category] = totals.get(category, 0.0) + record["value"]

        if progress_callback is not None:
            progress_callback(int(index / count * 100))

    return {
        "record_count": count,
        "totals_by_category": totals,
        "grand_total": sum(totals.values()),
    }


def format_summary(summary: dict) -> str:
    lines = [f"Records processed: {summary['record_count']}"]
    for category, total in sorted(summary["totals_by_category"].items()):
        lines.append(f"{category}: {total:.2f}")
    lines.append(f"Grand total: {summary['grand_total']:.2f}")
    return "\n".join(lines)
