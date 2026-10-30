"""Modern Hex Dark Theme definitions and styling helpers for Tkinter / TTK."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class HexDarkTheme:
    """Design System Constants for Dark Cybersecurity aesthetics."""

    # Color Palette (Tailwind / GitHub Dark inspired)
    BG_DARK = "#0d1117"        # Primary Window Canvas
    BG_CARD = "#161b22"        # Panel / Card Background
    BG_INPUT = "#21262d"       # Input field Background
    BORDER = "#30363d"         # Subtle borders
    BORDER_FOCUS = "#58a6ff"   # Focused borders

    ACCENT_GREEN = "#2ea043"   # Primary Success Neon Green
    ACCENT_GREEN_HOVER = "#3fb950"
    ACCENT_BLUE = "#58a6ff"    # Primary Action Blue
    ACCENT_BLUE_HOVER = "#79c0ff"
    ACCENT_RED = "#f85149"     # Danger / Delete Red
    ACCENT_RED_HOVER = "#ff7b72"
    ACCENT_YELLOW = "#d29922"  # Warning Amber
    ACCENT_PURPLE = "#bc8cff"  # Info Purple

    TEXT_PRIMARY = "#f0f6fc"   # High contrast white
    TEXT_MUTED = "#8b949e"     # Subtle gray
    TEXT_DARK = "#0d1117"

    # Font Families & Sizes
    FONT_FAMILY = "Segoe UI"
    FONT_MONO = "Consolas"

    FONT_TITLE = (FONT_FAMILY, 16, "bold")
    FONT_HEADER = (FONT_FAMILY, 13, "bold")
    FONT_BODY = (FONT_FAMILY, 10, "normal")
    FONT_BODY_BOLD = (FONT_FAMILY, 10, "bold")
    FONT_SMALL = (FONT_FAMILY, 9, "normal")
    FONT_CODE = (FONT_MONO, 10, "normal")

    @classmethod
    def apply_ttk_theme(cls, root: tk.Tk) -> ttk.Style:
        """Applies consistent dark styling across TTK widgets."""
        root.configure(bg=cls.BG_DARK)
        style = ttk.Style(root)
        style.theme_use("clam")

        # General Frames
        style.configure("TFrame", background=cls.BG_DARK)
        style.configure("Card.TFrame", background=cls.BG_CARD)

        # Labels
        style.configure(
            "TLabel",
            background=cls.BG_DARK,
            foreground=cls.TEXT_PRIMARY,
            font=cls.FONT_BODY,
        )
        style.configure(
            "Card.TLabel",
            background=cls.BG_CARD,
            foreground=cls.TEXT_PRIMARY,
            font=cls.FONT_BODY,
        )
        style.configure(
            "Muted.TLabel",
            background=cls.BG_CARD,
            foreground=cls.TEXT_MUTED,
            font=cls.FONT_SMALL,
        )
        style.configure(
            "Header.TLabel",
            background=cls.BG_DARK,
            foreground=cls.ACCENT_GREEN,
            font=cls.FONT_TITLE,
        )

        # Buttons
        style.configure(
            "Accent.TButton",
            background=cls.ACCENT_GREEN,
            foreground=cls.TEXT_PRIMARY,
            font=cls.FONT_BODY_BOLD,
            borderwidth=0,
            padding=(12, 6),
        )
        style.map(
            "Accent.TButton",
            background=[("active", cls.ACCENT_GREEN_HOVER), ("pressed", cls.ACCENT_GREEN)],
        )

        style.configure(
            "Blue.TButton",
            background=cls.ACCENT_BLUE,
            foreground=cls.TEXT_DARK,
            font=cls.FONT_BODY_BOLD,
            borderwidth=0,
            padding=(10, 5),
        )
        style.map(
            "Blue.TButton",
            background=[("active", cls.ACCENT_BLUE_HOVER)],
        )

        style.configure(
            "Danger.TButton",
            background=cls.BG_INPUT,
            foreground=cls.ACCENT_RED,
            font=cls.FONT_BODY_BOLD,
            borderwidth=1,
            relief="flat",
            padding=(10, 5),
        )
        style.map(
            "Danger.TButton",
            background=[("active", cls.ACCENT_RED)],
            foreground=[("active", cls.TEXT_PRIMARY)],
        )

        style.configure(
            "Secondary.TButton",
            background=cls.BG_INPUT,
            foreground=cls.TEXT_PRIMARY,
            font=cls.FONT_BODY,
            borderwidth=1,
            relief="flat",
            padding=(10, 5),
        )
        style.map(
            "Secondary.TButton",
            background=[("active", cls.BORDER)],
        )

        # Entry widgets
        style.configure(
            "TEntry",
            fieldbackground=cls.BG_INPUT,
            foreground=cls.TEXT_PRIMARY,
            bordercolor=cls.BORDER,
            lightcolor=cls.BORDER,
            darkcolor=cls.BORDER,
            padding=6,
        )

        # Treeview (Vault Credentials Table)
        style.configure(
            "Treeview",
            background=cls.BG_CARD,
            foreground=cls.TEXT_PRIMARY,
            fieldbackground=cls.BG_CARD,
            bordercolor=cls.BORDER,
            font=cls.FONT_BODY,
            rowheight=32,
        )
        style.map(
            "Treeview",
            background=[("selected", cls.BG_INPUT)],
            foreground=[("selected", cls.ACCENT_BLUE)],
        )
        style.configure(
            "Treeview.Heading",
            background=cls.BG_DARK,
            foreground=cls.TEXT_MUTED,
            font=cls.FONT_BODY_BOLD,
            relief="flat",
            padding=6,
        )
        style.map(
            "Treeview.Heading",
            background=[("active", cls.BG_INPUT)],
        )

        # Notebook (Tabs)
        style.configure("TNotebook", background=cls.BG_DARK, borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=cls.BG_INPUT,
            foreground=cls.TEXT_MUTED,
            font=cls.FONT_BODY_BOLD,
            padding=(16, 8),
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", cls.BG_CARD)],
            foreground=[("selected", cls.ACCENT_GREEN)],
        )

        return style
