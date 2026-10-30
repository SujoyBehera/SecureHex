"""Credential object hierarchy demonstrating OOP paradigms:
- Abstract Base Class (Credential)
- Encapsulation & Polymorphism
- Tagging / Marker Protocol (Auditable)
- Specialized subclasses: WebCredential, CardCredential, SecureNote
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Protocol, runtime_checkable
import uuid


@runtime_checkable
class Auditable(Protocol):
    """Marker/Tagging protocol for entities requiring periodic security audits."""

    def is_auditable(self) -> bool:
        ...


class Credential(ABC):
    """Abstract Base Class for all encrypted vault items."""

    def __init__(
        self,
        title: str,
        category: str,
        item_id: str | None = None,
        user_id: int | None = None,
        created_at: str | None = None,
        last_modified: str | None = None,
    ) -> None:
        self.id: str = item_id or str(uuid.uuid4())
        self.user_id: int | None = user_id
        self.title: str = title
        self.category: str = category
        self.created_at: str = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.last_modified: str = last_modified or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def touch(self) -> None:
        """Updates last modified timestamp to now."""
        self.last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Abstract Polymorphic Methods ---
    @abstractmethod
    def get_summary(self) -> str:
        """Returns non-sensitive metadata for dashboard display."""
        pass

    @abstractmethod
    def get_masked_details(self) -> str:
        """Returns obfuscated preview string."""
        pass

    @abstractmethod
    def get_primary_secret(self) -> str:
        """Returns the encrypted secret payload."""
        pass

    def is_auditable(self) -> bool:
        """Default Auditable implementation."""
        return True

    def __repr__(self) -> str:
        return f"[{self.category}] {self.title} (ID: {self.id[:8]}...)"


class WebCredential(Credential):
    """Web login credentials (Website, Username, Encrypted Password)."""

    def __init__(
        self,
        title: str,
        url: str,
        username: str,
        encrypted_password: str,
        item_id: str | None = None,
        user_id: int | None = None,
        created_at: str | None = None,
        last_modified: str | None = None,
    ) -> None:
        super().__init__(
            title=title,
            category="Web Login",
            item_id=item_id,
            user_id=user_id,
            created_at=created_at,
            last_modified=last_modified,
        )
        self.url = url
        self.username = username
        self.encrypted_password = encrypted_password

    def get_summary(self) -> str:
        return f"User: {self.username} | URL: {self.url}"

    def get_masked_details(self) -> str:
        return f"Username: {self.username} | Password: •••••••• ({self.url})"

    def get_primary_secret(self) -> str:
        return self.encrypted_password


class CardCredential(Credential):
    """Payment Card credentials (Cardholder, Encrypted Card Number, Expiry, Encrypted CVV)."""

    def __init__(
        self,
        title: str,
        cardholder_name: str,
        card_number_encrypted: str,
        expiry_date: str,
        cvv_encrypted: str,
        item_id: str | None = None,
        user_id: int | None = None,
        created_at: str | None = None,
        last_modified: str | None = None,
    ) -> None:
        super().__init__(
            title=title,
            category="Credit/Debit Card",
            item_id=item_id,
            user_id=user_id,
            created_at=created_at,
            last_modified=last_modified,
        )
        self.cardholder_name = cardholder_name
        self.card_number_encrypted = card_number_encrypted
        self.expiry_date = expiry_date
        self.cvv_encrypted = cvv_encrypted

    def get_summary(self) -> str:
        return f"Cardholder: {self.cardholder_name} | Exp: {self.expiry_date}"

    def get_masked_details(self) -> str:
        return f"Holder: {self.cardholder_name} | Number: •••• •••• •••• [Card] | Exp: {self.expiry_date}"

    def get_primary_secret(self) -> str:
        return self.card_number_encrypted


class SecureNote(Credential):
    """Secure encrypted note entity with categorizing tags."""

    def __init__(
        self,
        title: str,
        encrypted_note: str,
        tags: str = "",
        item_id: str | None = None,
        user_id: int | None = None,
        created_at: str | None = None,
        last_modified: str | None = None,
    ) -> None:
        super().__init__(
            title=title,
            category="Secure Note",
            item_id=item_id,
            user_id=user_id,
            created_at=created_at,
            last_modified=last_modified,
        )
        self.encrypted_note = encrypted_note
        self.tags = tags

    def get_summary(self) -> str:
        return f"Tags: [{self.tags or 'None'}]"

    def get_masked_details(self) -> str:
        return f"Encrypted Note Content [Hidden] | Tags: {self.tags}"

    def get_primary_secret(self) -> str:
        return self.encrypted_note
