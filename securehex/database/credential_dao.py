"""Data Access Object (DAO) for polymorphic Credential entities using SQLite."""

from __future__ import annotations

import sqlite3
from securehex.database.db_manager import DatabaseManager
from securehex.models.credential import (
    CardCredential,
    Credential,
    SecureNote,
    WebCredential,
)


class CredentialDAO:
    """Provides persistence, retrieval, and querying for encrypted credentials."""

    def __init__(self, db_manager: type[DatabaseManager] | None = None) -> None:
        self.db_manager = db_manager or DatabaseManager

    def save(self, user_id: int, credential: Credential) -> bool:
        """Inserts or updates a credential polymorphically into SQLite."""
        sql = """
            INSERT INTO credentials (
                id, user_id, title, category, field1, field2, secret_data, extra_data, created_at, last_modified
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                category = excluded.category,
                field1 = excluded.field1,
                field2 = excluded.field2,
                secret_data = excluded.secret_data,
                extra_data = excluded.extra_data,
                last_modified = excluded.last_modified
        """
        field1: str | None = None
        field2: str | None = None
        secret_data: str = credential.get_primary_secret()
        extra_data: str | None = None

        if isinstance(credential, WebCredential):
            field1 = credential.url
            field2 = credential.username
        elif isinstance(credential, CardCredential):
            field1 = credential.cardholder_name
            field2 = credential.expiry_date
            extra_data = credential.cvv_encrypted
        elif isinstance(credential, SecureNote):
            extra_data = credential.tags

        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                sql,
                (
                    credential.id,
                    user_id,
                    credential.title,
                    credential.category,
                    field1,
                    field2,
                    secret_data,
                    extra_data,
                    credential.created_at,
                    credential.last_modified,
                ),
            )
            return cursor.rowcount > 0

    def find_by_user_id(self, user_id: int) -> list[Credential]:
        """Retrieves and polymorphically instantiates all credentials for a given user."""
        sql = """
            SELECT id, user_id, title, category, field1, field2, secret_data, extra_data, created_at, last_modified
            FROM credentials
            WHERE user_id = ?
            ORDER BY last_modified DESC
        """
        results: list[Credential] = []
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (user_id,))
            rows = cursor.fetchall()
            for row in rows:
                cred = self._map_row_to_credential(row)
                if cred:
                    results.append(cred)
        return results

    def find_by_id(self, item_id: str) -> Credential | None:
        """Finds a specific credential by primary UUID."""
        sql = """
            SELECT id, user_id, title, category, field1, field2, secret_data, extra_data, created_at, last_modified
            FROM credentials
            WHERE id = ? LIMIT 1
        """
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (item_id,))
            row = cursor.fetchone()
            if row:
                return self._map_row_to_credential(row)
        return None

    def delete(self, item_id: str, user_id: int) -> bool:
        """Deletes a credential belonging to a specific user (prevents IDOR)."""
        sql = "DELETE FROM credentials WHERE id = ? AND user_id = ?"
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (item_id, user_id))
            return cursor.rowcount > 0

    def search(self, user_id: int, query: str) -> list[Credential]:
        """Performs a search query across titles and fields for a user."""
        sql = """
            SELECT id, user_id, title, category, field1, field2, secret_data, extra_data, created_at, last_modified
            FROM credentials
            WHERE user_id = ? AND (
                title LIKE ? OR category LIKE ? OR field1 LIKE ? OR field2 LIKE ? OR extra_data LIKE ?
            )
            ORDER BY last_modified DESC
        """
        term = f"%{query.strip()}%"
        results: list[Credential] = []
        with self.db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (user_id, term, term, term, term, term))
            for row in cursor.fetchall():
                cred = self._map_row_to_credential(row)
                if cred:
                    results.append(cred)
        return results

    @staticmethod
    def _map_row_to_credential(row: sqlite3.Row) -> Credential | None:
        """Factory method performing dynamic polymorphic instantiation from SQLite row."""
        category = row["category"]
        item_id = row["id"]
        user_id = row["user_id"]
        title = row["title"]
        created_at = row["created_at"]
        last_modified = row["last_modified"]

        if category == "Web Login":
            return WebCredential(
                title=title,
                url=row["field1"] or "",
                username=row["field2"] or "",
                encrypted_password=row["secret_data"],
                item_id=item_id,
                user_id=user_id,
                created_at=created_at,
                last_modified=last_modified,
            )
        elif category == "Credit/Debit Card":
            return CardCredential(
                title=title,
                cardholder_name=row["field1"] or "",
                expiry_date=row["field2"] or "",
                card_number_encrypted=row["secret_data"],
                cvv_encrypted=row["extra_data"] or "",
                item_id=item_id,
                user_id=user_id,
                created_at=created_at,
                last_modified=last_modified,
            )
        elif category == "Secure Note":
            return SecureNote(
                title=title,
                encrypted_note=row["secret_data"],
                tags=row["extra_data"] or "",
                item_id=item_id,
                user_id=user_id,
                created_at=created_at,
                last_modified=last_modified,
            )
        return None
