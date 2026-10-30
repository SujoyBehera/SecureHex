"""Cryptographic Password Hashing Service.

Demonstrates:
- Salted SHA-256 password hashing.
- Cryptographically secure pseudo-random number generator (CSPRNG) salts.
- Constant-time string comparison (hmac.compare_digest) to eliminate timing attacks.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os


class PasswordHasher:
    """Provides salted hashing and verification for vault master passwords."""

    @staticmethod
    def generate_salt(byte_length: int = 16) -> str:
        """Generates a cryptographically strong random salt encoded in Base64."""
        salt_bytes = os.urandom(byte_length)
        return base64.b64encode(salt_bytes).decode("utf-8")

    @staticmethod
    def hash_password(password: str, salt_b64: str) -> str:
        """Hashes a plaintext password with a Base64 salt using SHA-256."""
        if password is None or salt_b64 is None:
            raise ValueError("Password and salt cannot be None")

        salt_bytes = base64.b64decode(salt_b64.encode("utf-8"))
        hasher = hashlib.sha256()
        hasher.update(salt_bytes)
        hasher.update(password.encode("utf-8"))
        return hasher.hexdigest()

    @staticmethod
    def verify_password(plain_password: str, stored_hash: str, salt_b64: str) -> bool:
        """Verifies a password against the stored hash in constant time."""
        if not plain_password or not stored_hash or not salt_b64:
            return False
        computed_hash = PasswordHasher.hash_password(plain_password, salt_b64)
        return hmac.compare_digest(computed_hash, stored_hash)
