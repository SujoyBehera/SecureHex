"""Dynamic Password Strength Meter Canvas.

Demonstrating Syllabus:
Unit-5: Automata Based Programming Paradigm - Real-time DFA state rendering.
Provides real-time feedback bar with state colors and description labels.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from securehex.automata.password_dfa import PasswordDFA
from securehex.gui.theme import HexDarkTheme


class PasswordStrengthMeter(tk.Frame):
    """Custom Tkinter Widget showing dynamic DFA password complexity."""

    def __init__(self, parent: tk.Widget, *args, **kwargs) -> None:
        super().__init__(parent, bg=HexDarkTheme.BG_CARD, *args, **kwargs)

        self._build_ui()

    def _build_ui(self) -> None:
        # Progress canvas bar
        self.canvas = tk.Canvas(
            self,
            height=8,
            bg=HexDarkTheme.BG_INPUT,
            bd=0,
            highlightthickness=0,
            relief="flat",
        )
        self.canvas.pack(fill=tk.X, expand=True, pady=(2, 4))

        # Status text label
        self.status_label = tk.Label(
            self,
            text="DFA Status: Awaiting Input (Q_START)",
            font=HexDarkTheme.FONT_SMALL,
            fg=HexDarkTheme.TEXT_MUTED,
            bg=HexDarkTheme.BG_CARD,
            anchor="w",
        )
        self.status_label.pack(fill=tk.X)

        self.feedback_label = tk.Label(
            self,
            text="",
            font=HexDarkTheme.FONT_SMALL,
            fg=HexDarkTheme.ACCENT_YELLOW,
            bg=HexDarkTheme.BG_CARD,
            anchor="w",
            wraplength=380,
            justify="left",
        )
        self.feedback_label.pack(fill=tk.X, pady=(2, 0))

        # Draw empty baseline
        self.update_strength("")

    def update_strength(self, password: str) -> None:
        """Evaluates password using PasswordDFA and renders visual feedback."""
        dfa_result = PasswordDFA.evaluate(password)

        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        if width <= 1:
            width = 380  # fallback initial width

        fill_width = int((dfa_result.score / 100.0) * width)
        color = dfa_result.state.color_hex

        # Draw rounded bar
        if fill_width > 0:
            self.canvas.create_rectangle(
                0, 0, fill_width, 8, fill=color, outline=""
            )

        # Update labels
        state_text = f"DFA State: {dfa_result.state.name} ({dfa_result.score}% - {dfa_result.state.description})"
        self.status_label.configure(text=state_text, fg=color)

        if dfa_result.feedback:
            self.feedback_label.configure(text=" • " + " • ".join(dfa_result.feedback))
        else:
            self.feedback_label.configure(text="✔ Enterprise strength requirements met", fg=HexDarkTheme.ACCENT_GREEN)
