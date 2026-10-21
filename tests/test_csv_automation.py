import csv
import json
import tempfile
import unittest
from pathlib import Path

from csv_automation.report import build_report, summarize


class CsvAutomationTests(unittest.TestCase):
    def test_summary_groups_statuses(self) -> None:
        summary = summarize(
            [
                {"date": "2026-10-01", "category": "Bot", "amount": "100.50", "status": "Paid"},
                {"date": "2026-10-02", "category": "Site", "amount": "50", "status": "paid"},
                {"date": "2026-10-03", "category": "Audit", "amount": "25", "status": "pending"},
            ]
        )
        self.assertEqual(summary.rows, 3)
        self.assertEqual(summary.total, "175.50")
        self.assertEqual(summary.totals_by_status, {"paid": "150.50", "pending": "25.00"})

    def test_build_report_writes_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory, "input.csv")
            destination = Path(directory, "report.json")
            with source.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=["date", "category", "amount", "status"])
                writer.writeheader()
                writer.writerow({"date": "2026-10-01", "category": "Bot", "amount": "10", "status": "paid"})

            build_report(source, destination)
            self.assertEqual(json.loads(destination.read_text(encoding="utf-8"))["total"], "10.00")

    def test_invalid_amount_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "invalid amount"):
            summarize([{"date": "2026-10-01", "category": "Bot", "amount": "wrong", "status": "paid"}])

    def test_missing_column_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory, "input.csv")
            destination = Path(directory, "report.json")
            source.write_text("date,category,amount\n2026-10-01,Bot,10\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Missing columns: status"):
                build_report(source, destination)


if __name__ == "__main__":
    unittest.main()

