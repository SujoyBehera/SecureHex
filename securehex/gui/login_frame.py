"""Authentication View (Login and Registration Cards).

Demonstrating Syllabus:
Unit-2: Procedural Input Validation, Regex, Password Hashing.
Unit-3: Tkinter GUI MVC Architecture, Event-Driven Programming.
Unit-5: Real-time DFA Password validation during account registration.
"""

from __future__ import annotations

import re
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from securehex.database.user_dao import UserDAO
from securehex.gui.password_meter import PasswordStrengthMeter
from securehex.gui.theme import HexDarkTheme
from securehex.models.user import User
from securehex.security.hasher import PasswordHasher


class LoginRegisterFrame(tk.Frame):
    """View managing Sign-In and Registration cards with DFA meter and attempt limit."""

    MAX_LOGIN_ATTEMPTS = 5

    def __init__(
        self,
        parent: tk.Widget,
        user_dao: UserDAO,
        on_login_success: Callable[[User, str], None],
    ) -> None:
        super().__init__(parent, bg=HexDarkTheme.BG_DARK)
        self.user_dao = user_dao
        self.on_login_success = on_login_success
        self.remaining_attempts = self.MAX_LOGIN_ATTEMPTS

        self._build_ui()

    def _build_ui(self) -> None:
        # Centered container card
        center_wrapper = tk.Frame(self, bg=HexDarkTheme.BG_DARK)
        center_wrapper.place(relx=0.5, rely=0.5, anchor="center")

        card = tk.Frame(center_wrapper, bg=HexDarkTheme.BG_CARD, padx=32, pady=28)
        card.pack()

        # Branding Header
        brand_lbl = tk.Label(
            card,
            text="🛡️ SecureHex",
            font=(HexDarkTheme.FONT_FAMILY, 20, "bold"),
            fg=HexDarkTheme.ACCENT_GREEN,
            bg=HexDarkTheme.BG_CARD,
        )
        brand_lbl.pack(pady=(0, 2))

        sub_lbl = tk.Label(
            card,
            text="Enterprise Credential Management System (Python GUI Edition)",
            font=HexDarkTheme.FONT_SMALL,
            fg=HexDarkTheme.TEXT_MUTED,
            bg=HexDarkTheme.BG_CARD,
        )
        sub_lbl.pack(pady=(0, 16))

        # Tabbed Notebook for Sign In vs Register
        self.notebook = ttk.Notebook(card)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.login_tab = tk.Frame(self.notebook, bg=HexDarkTheme.BG_CARD, padx=16, pady=16)
        self._build_login_tab()
        self.notebook.add(self.login_tab, text="  Sign In  ")

        self.reg_tab = tk.Frame(self.notebook, bg=HexDarkTheme.BG_CARD, padx=16, pady=16)
        self._build_register_tab()
        self.notebook.add(self.reg_tab, text="  Create Account  ")

    def _build_login_tab(self) -> None:
        tk.Label(
            self.login_tab,
            text="Master Email Address:",
            font=HexDarkTheme.FONT_BODY,
            fg=HexDarkTheme.TEXT_MUTED,
            bg=HexDarkTheme.BG_CARD,
        ).pack(anchor="w", pady=(4, 2))

        self.login_email = ttk.Entry(self.login_tab, width=34)
        self.login_email.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            self.login_tab,
            text="Master Vault Password:",
            font=HexDarkTheme.FONT_BODY,
            fg=HexDarkTheme.TEXT_MUTED,
            bg=HexDarkTheme.BG_CARD,
        ).pack(anchor="w", pady=(0, 2))

        self.login_pwd = ttk.Entry(self.login_tab, show="•", width=34)
        self.login_pwd.pack(fill=tk.X, pady=(0, 12))
        self.login_pwd.bind("<Return>", lambda e: self._handle_login())

        self.attempt_lbl = tk.Label(
            self.login_tab,
            text=f"Attempts remaining: {self.remaining_attempts}",
            font=HexDarkTheme.FONT_SMALL,
            fg=HexDarkTheme.TEXT_MUTED,
            bg=HexDarkTheme.BG_CARD,
        )
        self.attempt_lbl.pack(anchor="w", pady=(0, 12))

        sign_in_btn = ttk.Button(
            self.login_tab,
            text="🔓 Unlock Master Vault",
            style="Accent.TButton",
            command=self._handle_login,
        )
        sign_in_btn.pack(fill=tk.X, pady=(4, 4))

    def _build_register_tab(self) -> None:
        tk.Label(self.reg_tab, text="Full Name:", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w", pady=(2, 2))
        self.reg_name = ttk.Entry(self.reg_tab, width=34)
        self.reg_name.pack(fill=tk.X, pady=(0, 8))

        tk.Label(self.reg_tab, text="Email Address:", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w", pady=(0, 2))
        self.reg_email = ttk.Entry(self.reg_tab, width=34)
        self.reg_email.pack(fill=tk.X, pady=(0, 8))

        tk.Label(self.reg_tab, text="Choose Master Password:", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w", pady=(0, 2))
        self.reg_pwd = ttk.Entry(self.reg_tab, show="•", width=34)
        self.reg_pwd.pack(fill=tk.X, pady=(0, 4))

        # Real-time DFA evaluation bar for registration
        self.reg_meter = PasswordStrengthMeter(self.reg_tab)
        self.reg_meter.pack(fill=tk.X, pady=(2, 8))
        self.reg_pwd.bind("<KeyRelease>", lambda e: self.reg_meter.update_strength(self.reg_pwd.get()))

        tk.Label(self.reg_tab, text="Confirm Master Password:", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w", pady=(0, 2))
        self.reg_confirm = ttk.Entry(self.reg_tab, show="•", width=34)
        self.reg_confirm.pack(fill=tk.X, pady=(0, 12))
        self.reg_confirm.bind("<Return>", lambda e: self._handle_register())

        reg_btn = ttk.Button(
            self.reg_tab,
            text="✨ Initialize Secure Vault",
            style="Blue.TButton",
            command=self._handle_register,
        )
        reg_btn.pack(fill=tk.X, pady=(4, 0))

    def _handle_login(self) -> None:
        if self.remaining_attempts <= 0:
            messagebox.showerror(
                "Vault Locked",
                "Maximum login attempts exceeded. Please restart the application for security reasons.",
                parent=self,
            )
            return

        email = self.login_email.get().strip().lower()
        password = self.login_pwd.get()

        if not email or not password:
            messagebox.showwarning("Incomplete Fields", "Please enter both email and master password.", parent=self)
            return

        user = self.user_dao.find_by_email(email)
        if not user:
            self._record_failed_attempt()
            return

        if PasswordHasher.verify_password(password, user.password_hash, user.salt):
            self.user_dao.update_last_login(user.id)
            self.on_login_success(user, password)
        else:
            self._record_failed_attempt()

    def _record_failed_attempt(self) -> None:
        self.remaining_attempts -= 1
        self.attempt_lbl.configure(
            text=f"Attempts remaining: {self.remaining_attempts}",
            fg=HexDarkTheme.ACCENT_RED,
        )
        if self.remaining_attempts <= 0:
            messagebox.showerror("Access Denied", "Vault locked. Maximum attempts exceeded.", parent=self)
        else:
            messagebox.showerror(
                "Authentication Failed",
                f"Invalid email or master password. ({self.remaining_attempts} attempts left)",
                parent=self,
            )

    def _handle_register(self) -> None:
        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip().lower()
        pwd = self.reg_pwd.get()
        confirm = self.reg_confirm.get()

        if not name or not email or not pwd:
            messagebox.showwarning("Missing Information", "All registration fields are required.", parent=self)
            return

        # Email regex format validation
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.", parent=self)
            return

        if pwd != confirm:
            messagebox.showerror("Password Mismatch", "Passwords do not match.", parent=self)
            return

        if len(pwd) < 8:
            messagebox.showerror("Password Policy", "Master password must be at least 8 characters.", parent=self)
            return

        if self.user_dao.email_exists(email):
            messagebox.showerror("Account Exists", "An account with this email already exists.", parent=self)
            return

        # Salt and hash password
        salt = PasswordHasher.generate_salt()
        pwd_hash = PasswordHasher.hash_password(pwd, salt)

        new_user = self.user_dao.create_user(name=name, email=email, password_hash=pwd_hash, salt=salt)
        if new_user:
            messagebox.showinfo("Registration Successful", "Master Vault initialized! You can now log in.", parent=self)
            self.notebook.select(0)
            self.login_email.delete(0, tk.END)
            self.login_email.insert(0, email)
            self.login_pwd.delete(0, tk.END)
            self.login_pwd.focus_set()
        else:
            messagebox.showerror("Database Error", "Failed to create user account in SQLite.", parent=self)
