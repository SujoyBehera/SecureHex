"""Formal DFA States for Password Complexity State Machine.

Demonstrating Syllabus:
Unit-5: Automata Based Programming Paradigm - Finite State Automata (DFA).
"""

from __future__ import annotations

from enum import Enum


class DFAState(Enum):
    """Represents states in the 5-tuple DFA M = (Q, Σ, δ, q0, F)."""

    Q_START = ("START", "Start State (Empty)", 0, "#6b7280")
    Q_SHORT = ("SHORT", "Too Short (< 8 characters)", 15, "#ef4444")
    Q_WEAK = ("WEAK", "Weak - Insufficient variety", 35, "#f97316")
    Q_MODERATE = ("MODERATE", "Moderate Strength", 65, "#eab308")
    Q_STRONG = ("STRONG", "Strong Password", 85, "#10b981")
    Q_EXCELLENT = ("EXCELLENT", "Excellent / Enterprise Grade", 100, "#06b6d4")

    def __init__(self, state_name: str, description: str, base_score: int, color_hex: str):
        self.state_name = state_name
        self.description = description
        self.base_score = base_score
        self.color_hex = color_hex

    @property
    def is_accepted(self) -> bool:
        """Accept states F = {Q_MODERATE, Q_STRONG, Q_EXCELLENT}."""
        return self in (DFAState.Q_MODERATE, DFAState.Q_STRONG, DFAState.Q_EXCELLENT)
