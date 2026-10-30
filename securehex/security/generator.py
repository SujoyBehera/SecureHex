"""Secure Procedural Password Generator.

Demonstrates:
- High-entropy cryptographic pseudo-random generation using secrets.
- Dynamic character pool configuration (uppercase, lowercase, numbers, symbols).
- Guaranteed diversity and Fisher-Yates uniform shuffle.
- Information-theoretic entropy calculation (Shannon bits of entropy).
"""

from __future__ import annotations

import math
import secrets
import string


class PasswordGenerator:
    """Generates strong, cryptographically secure passwords."""

    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SPECIAL = "!@#$%^&*()-_=+[]{}|;:,.<>?"

    @classmethod
    def generate_default(cls) -> str:
        """Generates a standard 16-character high-entropy password."""
        return cls.generate(length=16, use_lower=True, use_upper=True, use_digits=True, use_special=True)

    @classmethod
    def generate(
        cls,
        length: int = 16,
        use_lower: bool = True,
        use_upper: bool = True,
        use_digits: bool = True,
        use_special: bool = True,
    ) -> str:
        """Generates a randomized password satisfying chosen constraints."""
        if length < 8:
            length = 8

        allowed_chars: list[str] = []
        guaranteed_chars: list[str] = []

        if use_lower:
            allowed_chars.extend(cls.LOWERCASE)
            guaranteed_chars.append(secrets.choice(cls.LOWERCASE))
        if use_upper:
            allowed_chars.extend(cls.UPPERCASE)
            guaranteed_chars.append(secrets.choice(cls.UPPERCASE))
        if use_digits:
            allowed_chars.extend(cls.DIGITS)
            guaranteed_chars.append(secrets.choice(cls.DIGITS))
        if use_special:
            allowed_chars.extend(cls.SPECIAL)
            guaranteed_chars.append(secrets.choice(cls.SPECIAL))

        # Fallback if no sets were enabled
        if not allowed_chars:
            allowed_chars.extend(cls.LOWERCASE + cls.DIGITS)
            guaranteed_chars.append(secrets.choice(cls.LOWERCASE))

        # Fill remaining slots from the full allowable pool
        remaining = length - len(guaranteed_chars)
        password_chars = guaranteed_chars + [secrets.choice(allowed_chars) for _ in range(remaining)]

        # Cryptographically secure shuffle to prevent predictable placement
        shuffler = secrets.SystemRandom()
        shuffler.shuffle(password_chars)

        return "".join(password_chars)

    @classmethod
    def calculate_entropy(cls, password: str) -> float:
        """Calculates information-theoretic entropy in bits for a password.

        Formula: Entropy = L * log2(R)
        where L is length and R is the size of the character pool used.
        """
        if not password:
            return 0.0

        pool_size = 0
        has_lower = any(c in cls.LOWERCASE for c in password)
        has_upper = any(c in cls.UPPERCASE for c in password)
        has_digit = any(c in cls.DIGITS for c in password)
        has_special = any(c in cls.SPECIAL or (not c.isalnum() and not c.isspace()) for c in password)

        if has_lower:
            pool_size += len(cls.LOWERCASE)
        if has_upper:
            pool_size += len(cls.UPPERCASE)
        if has_digit:
            pool_size += len(cls.DIGITS)
        if has_special:
            pool_size += len(cls.SPECIAL)

        if pool_size == 0:
            pool_size = 1

        return round(len(password) * math.log2(pool_size), 1)
