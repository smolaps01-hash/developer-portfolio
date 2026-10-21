import sqlite3
import tempfile
import unittest
from pathlib import Path

from telegram_lead_bot.core import Lead, LeadStore, normalize_phone


class TelegramLeadBotTests(unittest.TestCase):
    def test_phone_is_normalized(self) -> None:
        self.assertEqual(normalize_phone("+7 (900) 123-45-67"), "+79001234567")

    def test_short_phone_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            normalize_phone("123")

    def test_lead_is_saved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory, "leads.db")
            store = LeadStore(database)
            store.initialize()
            lead_id = store.add(Lead(42, "Павел", "+7 900 123-45-67", "Нужен бот"))

            with sqlite3.connect(database) as connection:
                row = connection.execute(
                    "SELECT telegram_user_id, name, phone, comment FROM leads WHERE id = ?", (lead_id,)
                ).fetchone()

            self.assertEqual(row, (42, "Павел", "+79001234567", "Нужен бот"))


if __name__ == "__main__":
    unittest.main()

