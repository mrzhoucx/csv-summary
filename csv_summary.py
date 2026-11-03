#!/usr/bin/env python3
"""Summarize a CSV file: row/column counts and per-column stats.

Zero-dependency. Numeric columns get min/max/mean; text columns get the
number of distinct values plus the most common value. Missing cells are
counted separately so dirty data stays visible.

Usage:
    python3 csv_summary.py data.csv
    python3 csv_summary.py data.csv --json
    python3 csv_summary.py data.csv --top 5
"""

import argparse
import csv
import json
import sys
from collections import Counter


def _is_number(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def summarize(path, top=3):
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            return {"file": path, "rows": 0, "columns": []}
        columns = {name: [] for name in reader.fieldnames}
        rows = 0
        for row in reader:
            rows += 1
            for name in reader.fieldnames:
                columns[name].append(row.get(name))

    summary = {"file": path, "rows": rows, "columns": []}
    for name, values in columns.items():
        present = [v for v in values if v is not None and v.strip() != ""]
        col = {
            "name": name,
            "missing": len(values) - len(present),
            "distinct": len(set(present)),
        }
        if present and all(_is_number(v) for v in present):
            nums = [float(v) for v in present]
            col["type"] = "number"
            col["min"] = min(nums)
            col["max"] = max(nums)
            col["mean"] = round(sum(nums) / len(nums), 4)
        else:
            col["type"] = "text"
            col["most_common"] = Counter(present).most_common(top)
        summary["columns"].append(col)
    return summary


def render_text(summary):
    lines = [f"{summary['file']}: {summary['rows']} rows, "
             f"{len(summary['columns'])} columns"]
    for col in summary["columns"]:
        base = (f"  {col['name']} ({col['type']}, missing={col['missing']}, "
                f"distinct={col['distinct']})")
        if col["type"] == "number":
            lines.append(f"{base}: min={col['min']} max={col['max']} "
                         f"mean={col['mean']}")
        else:
            common = ", ".join(f"{v} x{n}" for v, n in col["most_common"])
            lines.append(f"{base}: most common: {common}" if common else base)
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Summarize a CSV file.")
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("--json", action="store_true",
                        help="Print the summary as JSON")
    parser.add_argument("--top", type=int, default=3,
                        help="How many most-common values to show (default: 3)")
    args = parser.parse_args(argv)
    try:
        summary = summarize(args.csv_file, top=args.top)
    except FileNotFoundError:
        print(f"error: file not found: {args.csv_file}", file=sys.stderr)
        return 1
    except csv.Error as exc:
        print(f"error: cannot parse CSV: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(summary, indent=2, ensure_ascii=False) if args.json
          else render_text(summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
