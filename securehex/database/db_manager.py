"""SQLite Database Connection and Schema Lifecycle Manager.

Demonstrates:
- Declarative SQLite persistence with transaction safety.
- Prepared statement queries and foreign key constraints.
- Auto-initialization and migration logic.
"""

from __future__ import annotations

from contextlib import contextmanager
import os
from pathlib import Path
import sqlite3
from typing import Generator

# Default DB Path stored alongside the repo root or user home
DEFAULT_DB_FILENAME = "securehex.db"


class DatabaseManager:
    """Manages SQLite database connectivity and schema lifecycle."""

    _db_path: str = DEFAULT_DB_FILENAME
    _initialized: bool = False

    @classmethod
    def set_db_path(cls, path: str | Path) -> None:
        """Sets the active database file path."""
        cls._db_path = str(path)
        cls._initialized = False

    @classmethod
    def get_db_path(cls) -> str:
        """Returns the absolute path to the active database file."""
        return os.path.abspath(cls._db_path)

    @classmethod
    @contextmanager
    def get_connection(cls) -> Generator[sqlite3.Connection, None, None]:
        """Context manager yielding a transactional SQLite connection with foreign keys enabled."""
        if not cls._initialized:
            cls.initialize()

        conn = sqlite3.connect(cls._db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @classmethod
    def initialize(cls, db_path: str | Path | None = None) -> None:
        """Initializes tables in the SQLite database if they do not exist."""
        if db_path is not None:
            cls._db_path = str(db_path)

        conn = sqlite3.connect(cls._db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Users table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT NOT NULL
            );
            """
        )

        # Credentials table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS credentials (
                id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                field1 TEXT,
                field2 TEXT,
                secret_data TEXT NOT NULL,
                extra_data TEXT,
                created_at TEXT NOT NULL,
                last_modified TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """
        )

        # Indexes for fast search
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_credentials_user ON credentials(user_id);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_credentials_cat ON credentials(category);"
        )

        conn.commit()
        conn.close()
        cls._initialized = True
