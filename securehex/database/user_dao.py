"""Data Access Object (DAO) for User entities using SQLite."""

from __future__ import annotations

from datetime import datetime
from securehex.database.db_manager import DatabaseManager
from securehex.models.user import User


class UserDAO:
    """Provides CRUD operations and authentication queries for Users in SQLite."""

    def __init__(self, db_manager: type[DatabaseManager] | None = None) -> None:
        self.db_manager = db_manager or DatabaseManager

    def create_user(self, name: str, email: str, password_hash: str, salt: str) -> User | None:
        """Inserts a new user record into the SQLite database.

        Returns the hydrated User model with assigned ID, or None if email already exists.
        """
        normalized_email = email.strip().lower()
        now = datetime.now().isoformat()

        sql = """
            INSERT INTO users (name, email, password_hash, salt, created_at, last_login)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        try:
            with self.db_manager.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (name.strip(), normalized_email, password_hash, salt, now, now))
                user_id = cursor.lastrowid
                return User(
                    id=user_id,
                    name=name.strip(),
                    email=normalized_email,
                    password_hash=password_hash,
                    salt=salt,
                    created_at=now,
                    last_login=now,
                )
        except Exception:
            # Handles UNIQUE constraint violations (email already taken)
            return None

    def find_by_email(self, email: str) -> User | None:
        """Finds a user by email address."""
        sql = "SELECT id, name, email, password_hash, salt, created_at, last_login FROM users WHERE email = ? LIMIT 1"
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (email.strip().lower(),))
            row = cursor.fetchone()
            if row:
                return User(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    password_hash=row["password_hash"],
                    salt=row["salt"],
                    created_at=row["created_at"],
                    last_login=row["last_login"],
                )
        return None

    def find_by_id(self, user_id: int) -> User | None:
        """Finds a user by primary key ID."""
        sql = "SELECT id, name, email, password_hash, salt, created_at, last_login FROM users WHERE id = ? LIMIT 1"
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            row = cursor.fetchone()
            if row:
                return User(
                    id=row["id"],
                    name=row["name"],
                    email=row["email"],
                    password_hash=row["password_hash"],
                    salt=row["salt"],
                    created_at=row["created_at"],
                    last_login=row["last_login"],
                )
        return None

    def update_last_login(self, user_id: int) -> bool:
        """Updates user's last login timestamp."""
        now = datetime.now().isoformat()
        sql = "UPDATE users SET last_login = ? WHERE id = ?"
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (now, user_id))
            return cursor.rowcount > 0

    def email_exists(self, email: str) -> bool:
        """Checks if an email is already registered."""
        return self.find_by_email(email) is not None
