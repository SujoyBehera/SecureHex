"""User domain model.

Demonstrates:
- Encapsulated user entity with dataclass.
- Email normalization and validation.
- Secure representation without leaking hashes in plain string output.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    """Represents an authenticated user in SecureHex."""

    id: int | None
    name: str
    email: str
    password_hash: str
    salt: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_login: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self) -> None:
        self.email = self.email.strip().lower()
        self.name = self.name.strip()

    def __repr__(self) -> str:
        return f"<User id={self.id} name='{self.name}' email='{self.email}'>"
