"""SecureHex Main Application Window Controller.

Demonstrating Syllabus:
Unit-3: Java Swing / Tkinter MVC Architecture.
Manages screen transitions between Authentication (Login/Register) and Dashboard views.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from securehex.database.credential_dao import CredentialDAO
from securehex.database.db_manager import DatabaseManager
from securehex.database.user_dao import UserDAO
from securehex.gui.dashboard_frame import DashboardFrame
from securehex.gui.login_frame import LoginRegisterFrame
from securehex.gui.theme import HexDarkTheme
from securehex.models.user import User


class SecureHexApp(tk.Tk):
    """Root Application Window and View Controller for SecureHex."""

    def __init__(self, db_path: str | None = None) -> None:
        super().__init__()

        # Initialize SQLite database schema
        DatabaseManager.initialize(db_path=db_path)
        self.user_dao = UserDAO()
        self.credential_dao = CredentialDAO()

        # Window Setup
        self.title("SecureHex — Enterprise Credential Manager (Python GUI Edition)")
        self.geometry("1020x680")
        self.minsize(860, 580)
        self.configure(bg=HexDarkTheme.BG_DARK)

        # Apply Global Theme Styles
        HexDarkTheme.apply_ttk_theme(self)

        # Active Session State
        self.current_user: User | None = None
        self.current_master_password: str | None = None
        self.active_view: tk.Widget | None = None

        # Start with Login View
        self.show_login_view()

    def show_login_view(self) -> None:
        """Transitions to the Authentication View."""
        if self.active_view:
            self.active_view.destroy()

        self.current_user = None
        self.current_master_password = None

        self.active_view = LoginRegisterFrame(
            parent=self,
            user_dao=self.user_dao,
            on_login_success=self.on_login_success,
        )
        self.active_view.pack(fill=tk.BOTH, expand=True)

    def on_login_success(self, user: User, master_password: str) -> None:
        """Invoked when user successfully signs in."""
        self.current_user = user
        self.current_master_password = master_password
        self.show_dashboard_view()

    def show_dashboard_view(self) -> None:
        """Transitions to the authenticated Dashboard View."""
        if self.active_view:
            self.active_view.destroy()

        if not self.current_user or not self.current_master_password:
            self.show_login_view()
            return

        self.active_view = DashboardFrame(
            parent=self,
            user=self.current_user,
            master_password=self.current_master_password,
            credential_dao=self.credential_dao,
            on_lock=self.on_vault_lock,
            on_logout=self.show_login_view,
        )
        self.active_view.pack(fill=tk.BOTH, expand=True)

    def on_vault_lock(self) -> None:
        """Handles manual or auto-lock timeout by clearing memory secrets and switching to login."""
        self.current_master_password = None
        self.show_login_view()
