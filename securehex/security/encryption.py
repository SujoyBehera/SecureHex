"""Symmetric Cryptography Engine (AES-256-GCM).

Provides authenticated symmetric encryption for credentials, card numbers,
and secure notes using AES-256 in Galois/Counter Mode (GCM).
"""

from __future__ import annotations

import base64
import hashlib
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class EncryptionService:
    """AES-256-GCM Authenticated Encryption & Decryption Service."""

    IV_LENGTH_BYTES = 12

    @classmethod
    def _derive_key(cls, master_password: str) -> bytes:
        """Derives a deterministic 256-bit (32-byte) AES key from the master password."""
        return hashlib.sha256(master_password.encode("utf-8")).digest()

    @classmethod
    def encrypt(cls, plaintext: str | None, master_password: str) -> str | None:
        """Encrypts plaintext string using AES-256-GCM authenticated encryption.

        Returns a Base64-encoded payload containing:
            [12-byte IV] + [ciphertext + 16-byte authentication tag]
        """
        if plaintext is None:
            return None

        key = cls._derive_key(master_password)
        aesgcm = AESGCM(key)
        iv = os.urandom(cls.IV_LENGTH_BYTES)

        plaintext_bytes = plaintext.encode("utf-8")
        ciphertext_and_tag = aesgcm.encrypt(iv, plaintext_bytes, None)

        combined = iv + ciphertext_and_tag
        return base64.b64encode(combined).decode("utf-8")

    @classmethod
    def decrypt(cls, encrypted_b64: str | None, master_password: str) -> str | None:
        """Decrypts a Base64 payload containing IV and ciphertext with AES-256-GCM.

        Raises ValueError if authentication fails (wrong password or altered ciphertext).
        """
        if encrypted_b64 is None:
            return None

        try:
            combined = base64.b64decode(encrypted_b64.encode("utf-8"))
            if len(combined) < cls.IV_LENGTH_BYTES + 16:
                raise ValueError("Malformed encrypted payload")

            iv = combined[: cls.IV_LENGTH_BYTES]
            ciphertext_and_tag = combined[cls.IV_LENGTH_BYTES :]

            key = cls._derive_key(master_password)
            aesgcm = AESGCM(key)
            decrypted_bytes = aesgcm.decrypt(iv, ciphertext_and_tag, None)
            return decrypted_bytes.decode("utf-8")
        except Exception as exc:
            raise ValueError(f"Decryption failed (incorrect key or corrupted data): {exc}") from exc
