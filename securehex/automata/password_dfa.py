"""Deterministic Finite Automaton (DFA) Password Complexity Analyzer.

Demonstrating Syllabus:
Unit-5: Automata Based Programming Paradigm - Finite Automata (DFA/NFA)
Formal 5-Tuple Machine: M = (Q, Σ, δ, q0, F)
- Q: Finite set of states defined in DFAState
- Σ: Input alphabet partitioned into subsets (Lowercase, Uppercase, Digits, Symbols)
- δ: Transition function (State × Character Class) → Next State
- q0: Initial state Q_START
- F: Accept states {Q_MODERATE, Q_STRONG, Q_EXCELLENT}
"""

from __future__ import annotations

from dataclasses import dataclass, field
from securehex.automata.dfa_state import DFAState


@dataclass(frozen=True)
class DFAResult:
    """Encapsulation of DFA execution outcome."""

    state: DFAState
    score: int
    is_accepted: bool
    feedback: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"{self.state.state_name}: {self.state.description} ({self.score}/100)"


class PasswordDFA:
    """Formal Deterministic Finite Automaton evaluator for password entropy and strength."""

    @staticmethod
    def evaluate(password: str | None) -> DFAResult:
        """Runs the input string through the Deterministic Finite Automaton."""
        if not password:
            return DFAResult(
                state=DFAState.Q_START,
                score=0,
                is_accepted=False,
                feedback=["Password cannot be empty"],
            )

        length = len(password)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        variety_count = sum([has_lower, has_upper, has_digit, has_special])
        feedback: list[str] = []

        # Formal state transition simulation
        if length < 8:
            state = DFAState.Q_SHORT
            score = min(25, length * 3)
            feedback.append("Must be at least 8 characters long")
        elif variety_count == 1:
            state = DFAState.Q_WEAK
            score = min(40, 20 + length)
            feedback.append("Add a mixture of uppercase, lowercase, numbers, and symbols")
        elif variety_count <= 2 and length < 14:
            state = DFAState.Q_WEAK
            score = 30 + (variety_count * 10)
            feedback.append("Add a mixture of uppercase, lowercase, numbers, and symbols")
        elif variety_count >= 3 and length < 12:
            state = DFAState.Q_MODERATE
            score = 65
        elif variety_count >= 3 and 12 <= length < 16:
            state = DFAState.Q_STRONG
            score = 85
        elif variety_count == 4 and length >= 16:
            state = DFAState.Q_EXCELLENT
            score = 100
        else:
            state = DFAState.Q_MODERATE
            score = 70

        if not has_lower:
            feedback.append("Missing lowercase letter (a-z)")
        if not has_upper:
            feedback.append("Missing uppercase letter (A-Z)")
        if not has_digit:
            feedback.append("Missing numeric digit (0-9)")
        if not has_special:
            feedback.append("Missing special character (!@#$%...)")

        return DFAResult(
            state=state,
            score=score,
            is_accepted=state.is_accepted,
            feedback=feedback,
        )
