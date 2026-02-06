import sqlite3
from pathlib import Path
from typing import Iterable

from scanner.models import ScoredCandidate


class ScannerStorage:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id TEXT,
                source TEXT,
                lane TEXT,
                url TEXT,
                county TEXT,
                price REAL,
                sqft INTEGER,
                baths REAL,
                hoa INTEGER,
                cdd INTEGER,
                address TEXT,
                decision TEXT,
                score INTEGER,
                reasons TEXT,
                scanned_at TEXT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS seen_identifiers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id TEXT,
                url TEXT,
                first_seen_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(listing_id),
                UNIQUE(url)
            )
            """
        )
        self.conn.commit()

    def has_seen(self, listing_id: str, url: str) -> bool:
        cur = self.conn.cursor()
        cur.execute(
            "SELECT 1 FROM seen_identifiers WHERE listing_id = ? OR url = ? LIMIT 1",
            (listing_id, url),
        )
        return cur.fetchone() is not None

    def mark_seen(self, listing_id: str, url: str) -> None:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO seen_identifiers (listing_id, url) VALUES (?, ?)",
            (listing_id, url),
        )
        self.conn.commit()

    def insert_scored_candidates(self, scored_candidates: Iterable[ScoredCandidate]) -> None:
        cur = self.conn.cursor()
        for scored in scored_candidates:
            c = scored.candidate
            cur.execute(
                """
                INSERT INTO candidates (
                    listing_id, source, lane, url, county, price, sqft, baths,
                    hoa, cdd, address, decision, score, reasons, scanned_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    c.listing_id,
                    c.source,
                    c.lane,
                    c.url,
                    c.county,
                    c.price,
                    c.sqft,
                    c.baths,
                    int(c.hoa) if c.hoa is not None else None,
                    int(c.cdd) if c.cdd is not None else None,
                    c.address,
                    scored.decision,
                    scored.score,
                    " | ".join(scored.reasons),
                    c.scanned_at.isoformat(),
                ),
            )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()
