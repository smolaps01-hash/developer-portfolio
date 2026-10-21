from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path


PHONE_PATTERN = re.compile(r"^\+?[0-9][0-9 ()-]{8,18}$")


@dataclass(frozen=True)
class Lead:
    telegram_user_id: int
    name: str
    phone: str
    comment: str


def normalize_phone(value: str) -> str:
    value = value.strip()
    if not PHONE_PATTERN.fullmatch(value):
        raise ValueError("Phone must contain 9–19 digits or formatting characters")
    digits = re.sub(r"\D", "", value)
    if not 9 <= len(digits) <= 15:
        raise ValueError("Phone must contain 9–15 digits")
    return f"+{digits}"


class LeadStore:
    def __init__(self, database: Path | str) -> None:
        self.database = str(database)

    def initialize(self) -> None:
        with sqlite3.connect(self.database) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    comment TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add(self, lead: Lead) -> int:
        with sqlite3.connect(self.database) as connection:
            cursor = connection.execute(
                "INSERT INTO leads (telegram_user_id, name, phone, comment) VALUES (?, ?, ?, ?)",
                (lead.telegram_user_id, lead.name.strip(), normalize_phone(lead.phone), lead.comment.strip()),
            )
            return int(cursor.lastrowid)

