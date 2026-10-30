"""Interactive Password Generator Dialog.

Provides real-time entropy calculation, character pool toggling, length slider,
and one-click clipboard copying.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from securehex.gui.password_meter import PasswordStrengthMeter
from securehex.gui.theme import HexDarkTheme
from securehex.security.generator import PasswordGenerator


class PasswordGeneratorDialog(tk.Toplevel):
    """Standalone interactive password generator with live entropy metrics."""

    def __init__(self, parent: tk.Widget) -> None:
        super().__init__(parent)
        self.title("SecureHex — High-Entropy Password Generator")
        self.geometry("480x420")
        self.resizable(False, False)
        self.configure(bg=HexDarkTheme.BG_DARK)
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._generate()

    def _build_ui(self) -> None:
        container = tk.Frame(self, bg=HexDarkTheme.BG_CARD, padx=20, pady=18)
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        tk.Label(
            container,
            text="⚡ Cryptographic Password Generator",
            font=HexDarkTheme.FONT_TITLE,
            fg=HexDarkTheme.ACCENT_GREEN,
            bg=HexDarkTheme.BG_CARD,
        ).pack(anchor="w", pady=(0, 10))

        # Output Display & Copy Button
        out_frame = tk.Frame(container, bg=HexDarkTheme.BG_CARD)
        out_frame.pack(fill=tk.X, pady=(0, 8))

        self.pwd_entry = ttk.Entry(out_frame, font=HexDarkTheme.FONT_CODE)
        self.pwd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        copy_btn = ttk.Button(out_frame, text="📋 Copy", style="Blue.TButton", command=self._copy_to_clipboard)
        copy_btn.pack(side=tk.RIGHT)

        # Entropy & Strength meter
        self.meter = PasswordStrengthMeter(container)
        self.meter.pack(fill=tk.X, pady=(0, 12))

        self.entropy_label = tk.Label(
            container,
            text="Shannon Entropy: Calculating...",
            font=HexDarkTheme.FONT_SMALL,
            fg=HexDarkTheme.ACCENT_PURPLE,
            bg=HexDarkTheme.BG_CARD,
            anchor="w",
        )
        self.entropy_label.pack(fill=tk.X, pady=(0, 10))

        # Slider for Length
        slider_frame = tk.Frame(container, bg=HexDarkTheme.BG_CARD)
        slider_frame.pack(fill=tk.X, pady=(0, 10))

        self.length_var = tk.IntVar(value=18)
        self.slider_label = tk.Label(
            slider_frame,
            text=f"Password Length: {self.length_var.get()}",
            font=HexDarkTheme.FONT_BODY_BOLD,
            fg=HexDarkTheme.TEXT_PRIMARY,
            bg=HexDarkTheme.BG_CARD,
        )
        self.slider_label.pack(anchor="w")

        slider = ttk.Scale(
            slider_frame,
            from_=8,
            to=64,
            variable=self.length_var,
            command=self._on_slider_change,
        )
        slider.pack(fill=tk.X, pady=(4, 0))

        # Checkbox Pool Options
        opts_frame = tk.Frame(container, bg=HexDarkTheme.BG_CARD)
        opts_frame.pack(fill=tk.X, pady=(0, 12))

        self.var_lower = tk.BooleanVar(value=True)
        self.var_upper = tk.BooleanVar(value=True)
        self.var_digits = tk.BooleanVar(value=True)
        self.var_special = tk.BooleanVar(value=True)

        for text, var in [
            ("Lowercase (a-z)", self.var_lower),
            ("Uppercase (A-Z)", self.var_upper),
            ("Numbers (0-9)", self.var_digits),
            ("Special Characters (!@#$)", self.var_special),
        ]:
            cb = tk.Checkbutton(
                opts_frame,
                text=text,
                variable=var,
                bg=HexDarkTheme.BG_CARD,
                fg=HexDarkTheme.TEXT_PRIMARY,
                selectcolor=HexDarkTheme.BG_INPUT,
                activebackground=HexDarkTheme.BG_CARD,
                activeforeground=HexDarkTheme.TEXT_PRIMARY,
                command=self._generate,
            )
            cb.pack(side=tk.LEFT, padx=(0, 8))

        # Bottom Regenerate & Close
        btn_bar = tk.Frame(container, bg=HexDarkTheme.BG_CARD)
        btn_bar.pack(fill=tk.X, pady=(8, 0))

        regen_btn = ttk.Button(btn_bar, text="🔄 Regenerate", style="Accent.TButton", command=self._generate)
        regen_btn.pack(side=tk.LEFT)

        close_btn = ttk.Button(btn_bar, text="Close", style="Secondary.TButton", command=self.destroy)
        close_btn.pack(side=tk.RIGHT)

    def _on_slider_change(self, val: str) -> None:
        int_val = int(float(val))
        self.slider_label.configure(text=f"Password Length: {int_val}")
        self._generate()

    def _generate(self) -> None:
        length = self.length_var.get()
        pwd = PasswordGenerator.generate(
            length=length,
            use_lower=self.var_lower.get(),
            use_upper=self.var_upper.get(),
            use_digits=self.var_digits.get(),
            use_special=self.var_special.get(),
        )
        self.pwd_entry.delete(0, tk.END)
        self.pwd_entry.insert(0, pwd)
        self.meter.update_strength(pwd)

        entropy = PasswordGenerator.calculate_entropy(pwd)
        self.entropy_label.configure(
            text=f"Shannon Entropy: {entropy} bits (2^{entropy} brute-force combinations)"
        )

    def _copy_to_clipboard(self) -> None:
        pwd = self.pwd_entry.get()
        if pwd:
            self.clipboard_clear()
            self.clipboard_append(pwd)
            messagebox.showinfo("Copied", "Generated password copied to clipboard!", parent=self)
