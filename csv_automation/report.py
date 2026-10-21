from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterable


REQUIRED_COLUMNS = {"date", "category", "amount", "status"}


@dataclass(frozen=True)
class Summary:
    rows: int
    total: str
    totals_by_status: dict[str, str]


def _money(value: Decimal) -> str:
    return f"{value.quantize(Decimal('0.01')):.2f}"


def summarize(rows: Iterable[dict[str, str]]) -> Summary:
    total = Decimal("0")
    totals_by_status: defaultdict[str, Decimal] = defaultdict(lambda: Decimal("0"))
    count = 0

    for line_number, row in enumerate(rows, start=2):
        missing = [column for column in REQUIRED_COLUMNS if not row.get(column, "").strip()]
        if missing:
            raise ValueError(f"Row {line_number}: empty values in {', '.join(sorted(missing))}")

        try:
            amount = Decimal(row["amount"].replace(",", "."))
        except InvalidOperation as exc:
            raise ValueError(f"Row {line_number}: invalid amount {row['amount']!r}") from exc

        status = row["status"].strip().lower()
        total += amount
        totals_by_status[status] += amount
        count += 1

    return Summary(
        rows=count,
        total=_money(total),
        totals_by_status={key: _money(totals_by_status[key]) for key in sorted(totals_by_status)},
    )


def build_report(source: Path, destination: Path) -> Summary:
    with source.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        columns = set(reader.fieldnames or [])
        missing_columns = REQUIRED_COLUMNS - columns
        if missing_columns:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing_columns))}")
        summary = summarize(reader)

    destination.write_text(
        json.dumps(asdict(summary), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a JSON summary from a CSV operations file.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=Path("report.json"))
    args = parser.parse_args()

    summary = build_report(args.source, args.output)
    print(f"Processed {summary.rows} rows. Total: {summary.total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

