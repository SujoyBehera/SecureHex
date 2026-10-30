"""SecureHex Main Vault Dashboard View.

Demonstrating Syllabus:
Unit-2: Polymorphism (dynamic method calls on Credential instances).
Unit-3: Concurrency (AutoLockManager inactivity daemon & SecurityAuditorThread worker).
Unit-3: Declarative Persistence (CredentialDAO queries on SQLite).
Unit-3: Tkinter GUI MVC Architecture with modern dark styling and clipboard wiping.
"""

from __future__ import annotations

import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Callable

from securehex.concurrency.autolock import AutoLockManager
from securehex.concurrency.security_auditor import AuditReport, SecurityAuditorThread
from securehex.database.credential_dao import CredentialDAO
from securehex.gui.add_dialog import AddCredentialDialog
from securehex.gui.audit_dialog import SecurityAuditDialog
from securehex.gui.generator_dialog import PasswordGeneratorDialog
from securehex.gui.theme import HexDarkTheme
from securehex.models.credential import CardCredential, Credential, SecureNote, WebCredential
from securehex.models.user import User
from securehex.security.encryption import EncryptionService


class DashboardFrame(tk.Frame):
    """Main application dashboard displaying credentials table, metrics, and actions."""

    CLIPBOARD_TIMEOUT_SECONDS = 30
    DEFAULT_INACTIVITY_TIMEOUT = 180  # 3 minutes

    def __init__(
        self,
        parent: tk.Widget,
        user: User,
        master_password: str,
        credential_dao: CredentialDAO,
        on_lock: Callable[[], None],
        on_logout: Callable[[], None],
    ) -> None:
        super().__init__(parent, bg=HexDarkTheme.BG_DARK)
        self.user = user
        self.master_password = master_password
        self.dao = credential_dao
        self.on_lock = on_lock
        self.on_logout = on_logout

        self.credentials: list[Credential] = []
        self.filtered_credentials: list[Credential] = []

        # Auto-Lock Concurrency Manager
        self.auto_lock = AutoLockManager(
            timeout_seconds=self.DEFAULT_INACTIVITY_TIMEOUT,
            lock_callback=self._on_auto_lock_triggered,
        )

        self._build_ui()
        self._setup_inactivity_bindings()
        self.reload_data()
        self.auto_lock.start()
        self._tick_countdown()

    def _build_ui(self) -> None:
        # 1. Header Toolbar
        header = tk.Frame(self, bg=HexDarkTheme.BG_CARD, padx=16, pady=12)
        header.pack(fill=tk.X, padx=12, pady=(12, 6))

        # Left Branding & User Info
        left_header = tk.Frame(header, bg=HexDarkTheme.BG_CARD)
        left_header.pack(side=tk.LEFT)

        logo_lbl = tk.Label(
            left_header,
            text="🛡️ SecureHex Vault",
            font=HexDarkTheme.FONT_TITLE,
            fg=HexDarkTheme.ACCENT_GREEN,
            bg=HexDarkTheme.BG_CARD,
        )
        logo_lbl.pack(side=tk.LEFT, padx=(0, 10))

        user_lbl = tk.Label(
            left_header,
            text=f"• Logged in as: {self.user.name} ({self.user.email})",
            font=HexDarkTheme.FONT_SMALL,
            fg=HexDarkTheme.TEXT_MUTED,
            bg=HexDarkTheme.BG_CARD,
        )
        user_lbl.pack(side=tk.LEFT)

        # Right Controls (Auto-Lock Timer, Lock, Logout)
        right_header = tk.Frame(header, bg=HexDarkTheme.BG_CARD)
        right_header.pack(side=tk.RIGHT)

        self.lock_timer_lbl = tk.Label(
            right_header,
            text="⏳ Auto-Lock: 180s",
            font=HexDarkTheme.FONT_CODE,
            fg=HexDarkTheme.TEXT_MUTED,
            bg=HexDarkTheme.BG_CARD,
        )
        self.lock_timer_lbl.pack(side=tk.LEFT, padx=(0, 12))

        lock_btn = ttk.Button(
            right_header,
            text="🔒 Lock Vault",
            style="Secondary.TButton",
            command=self.lock_vault,
        )
        lock_btn.pack(side=tk.LEFT, padx=(0, 6))

        logout_btn = ttk.Button(
            right_header,
            text="🚪 Logout",
            style="Danger.TButton",
            command=self.logout,
        )
        logout_btn.pack(side=tk.LEFT)

        # 2. Stats / Metrics Ribbon
        stats_frame = tk.Frame(self, bg=HexDarkTheme.BG_DARK)
        stats_frame.pack(fill=tk.X, padx=12, pady=(0, 6))

        self.stat_total = self._create_metric_card(stats_frame, "Total Items", "0", HexDarkTheme.ACCENT_BLUE)
        self.stat_web = self._create_metric_card(stats_frame, "Web Logins", "0", HexDarkTheme.ACCENT_GREEN)
        self.stat_cards = self._create_metric_card(stats_frame, "Payment Cards", "0", HexDarkTheme.ACCENT_YELLOW)
        self.stat_notes = self._create_metric_card(stats_frame, "Secure Notes", "0", HexDarkTheme.ACCENT_PURPLE)

        # 3. Search and Filter Bar
        filter_bar = tk.Frame(self, bg=HexDarkTheme.BG_CARD, padx=12, pady=8)
        filter_bar.pack(fill=tk.X, padx=12, pady=(0, 6))

        tk.Label(
            filter_bar,
            text="🔍 Search:",
            font=HexDarkTheme.FONT_BODY_BOLD,
            fg=HexDarkTheme.TEXT_MUTED,
            bg=HexDarkTheme.BG_CARD,
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.search_entry = ttk.Entry(filter_bar, width=32)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 12))
        self.search_entry.bind("<KeyRelease>", lambda e: self._apply_filter())

        tk.Label(
            filter_bar,
            text="Category:",
            font=HexDarkTheme.FONT_BODY_BOLD,
            fg=HexDarkTheme.TEXT_MUTED,
            bg=HexDarkTheme.BG_CARD,
        ).pack(side=tk.LEFT, padx=(0, 6))

        self.category_filter = ttk.Combobox(
            filter_bar,
            values=["All Categories", "Web Login", "Credit/Debit Card", "Secure Note"],
            state="readonly",
            width=18,
        )
        self.category_filter.set("All Categories")
        self.category_filter.pack(side=tk.LEFT)
        self.category_filter.bind("<<ComboboxSelected>>", lambda e: self._apply_filter())

        # 4. Central Treeview Table
        table_container = tk.Frame(self, bg=HexDarkTheme.BG_CARD)
        table_container.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 6))

        columns = ("type", "title", "details", "masked", "modified")
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("type", text="Type")
        self.tree.heading("title", text="Title / Service")
        self.tree.heading("details", text="Account / Resource Details")
        self.tree.heading("masked", text="Masked Secret")
        self.tree.heading("modified", text="Last Modified")

        self.tree.column("type", width=120, anchor="center")
        self.tree.column("title", width=180, anchor="w")
        self.tree.column("details", width=280, anchor="w")
        self.tree.column("masked", width=160, anchor="center")
        self.tree.column("modified", width=150, anchor="center")

        tree_scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", lambda e: self._reveal_selected_secret())

        # 5. Bottom Action Controls Bar
        action_bar = tk.Frame(self, bg=HexDarkTheme.BG_CARD, padx=12, pady=10)
        action_bar.pack(fill=tk.X, padx=12, pady=(0, 12))

        add_btn = ttk.Button(action_bar, text="➕ Add Item", style="Accent.TButton", command=self._open_add_dialog)
        add_btn.pack(side=tk.LEFT, padx=(0, 6))

        copy_btn = ttk.Button(action_bar, text="📋 Copy Secret", style="Blue.TButton", command=self._copy_selected_secret)
        copy_btn.pack(side=tk.LEFT, padx=(0, 6))

        reveal_btn = ttk.Button(action_bar, text="👁️ Reveal Secret", style="Secondary.TButton", command=self._reveal_selected_secret)
        reveal_btn.pack(side=tk.LEFT, padx=(0, 6))

        edit_btn = ttk.Button(action_bar, text="✏️ Edit", style="Secondary.TButton", command=self._open_edit_dialog)
        edit_btn.pack(side=tk.LEFT, padx=(0, 6))

        del_btn = ttk.Button(action_bar, text="🗑️ Delete", style="Danger.TButton", command=self._delete_selected)
        del_btn.pack(side=tk.LEFT, padx=(0, 6))

        gen_btn = ttk.Button(action_bar, text="⚡ Password Generator", style="Secondary.TButton", command=self._open_generator)
        gen_btn.pack(side=tk.LEFT, padx=(0, 6))

        audit_btn = ttk.Button(action_bar, text="🛡️ Run Security Audit (Multithreaded)", style="Accent.TButton", command=self._run_multithreaded_audit)
        audit_btn.pack(side=tk.RIGHT)

        backup_btn = ttk.Button(action_bar, text="💾 Backup JSON", style="Secondary.TButton", command=self._export_vault)
        backup_btn.pack(side=tk.RIGHT, padx=(0, 6))

    def _create_metric_card(self, parent: tk.Widget, title: str, val: str, color: str) -> tk.Label:
        card = tk.Frame(parent, bg=HexDarkTheme.BG_CARD, padx=14, pady=8)
        card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        tk.Label(card, text=title, font=HexDarkTheme.FONT_SMALL, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w")
        val_lbl = tk.Label(card, text=val, font=HexDarkTheme.FONT_TITLE, fg=color, bg=HexDarkTheme.BG_CARD)
        val_lbl.pack(anchor="w")
        return val_lbl

    def _setup_inactivity_bindings(self) -> None:
        """Binds user input events to reset the auto-lock activity timer."""
        toplevel = self.winfo_toplevel()
        toplevel.bind_all("<Key>", lambda e: self.auto_lock.record_activity())
        toplevel.bind_all("<Button>", lambda e: self.auto_lock.record_activity())
        toplevel.bind_all("<Motion>", lambda e: self.auto_lock.record_activity())

    def _tick_countdown(self) -> None:
        """Refreshes remaining auto-lock countdown timer label every second."""
        if self.winfo_exists():
            secs = self.auto_lock.get_remaining_seconds()
            self.lock_timer_lbl.configure(text=f"⏳ Auto-Lock: {secs}s")
            self.after(1000, self._tick_countdown)

    def _on_auto_lock_triggered(self) -> None:
        """Callback from background AutoLock thread."""
        self.after(0, self.lock_vault)

    def reload_data(self) -> None:
        """Fetches fresh data from SQLite via CredentialDAO and updates UI."""
        self.credentials = self.dao.find_by_user_id(self.user.id)
        self._apply_filter()
        self._update_metrics()

    def _update_metrics(self) -> None:
        total = len(self.credentials)
        web_count = sum(1 for c in self.credentials if isinstance(c, WebCredential))
        card_count = sum(1 for c in self.credentials if isinstance(c, CardCredential))
        note_count = sum(1 for c in self.credentials if isinstance(c, SecureNote))

        self.stat_total.configure(text=str(total))
        self.stat_web.configure(text=str(web_count))
        self.stat_cards.configure(text=str(card_count))
        self.stat_notes.configure(text=str(note_count))

    def _apply_filter(self) -> None:
        query = self.search_entry.get().strip().lower()
        selected_cat = self.category_filter.get()

        self.tree.delete(*self.tree.get_children())
        self.filtered_credentials = []

        for cred in self.credentials:
            if selected_cat != "All Categories" and cred.category != selected_cat:
                continue

            # Query match across title and summary details
            summary = cred.get_summary().lower()
            title = cred.title.lower()
            if query and (query not in title and query not in summary):
                continue

            self.filtered_credentials.append(cred)
            self.tree.insert(
                "",
                tk.END,
                iid=cred.id,
                values=(
                    cred.category,
                    cred.title,
                    cred.get_summary(),
                    "••••••••",
                    cred.last_modified,
                ),
            )

    def _get_selected_credential(self) -> Credential | None:
        selected_ids = self.tree.selection()
        if not selected_ids:
            messagebox.showwarning("Select Item", "Please select a vault item first.", parent=self)
            return None
        cred_id = selected_ids[0]
        return self.dao.find_by_id(cred_id)

    def _open_add_dialog(self) -> None:
        AddCredentialDialog(
            parent=self,
            user=self.user,
            master_password=self.master_password,
            credential_dao=self.dao,
            on_saved_callback=self.reload_data,
        )

    def _open_edit_dialog(self) -> None:
        cred = self._get_selected_credential()
        if not cred:
            return
        AddCredentialDialog(
            parent=self,
            user=self.user,
            master_password=self.master_password,
            credential_dao=self.dao,
            on_saved_callback=self.reload_data,
            credential_to_edit=cred,
        )

    def _delete_selected(self) -> None:
        cred = self._get_selected_credential()
        if not cred:
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to permanently delete '{cred.title}'?",
            parent=self,
        )
        if confirm:
            self.dao.delete(cred.id, self.user.id)
            self.reload_data()

    def _copy_selected_secret(self) -> None:
        cred = self._get_selected_credential()
        if not cred:
            return

        try:
            decrypted = EncryptionService.decrypt(cred.get_primary_secret(), self.master_password)
            if not decrypted:
                messagebox.showerror("Decryption Failed", "Unable to decrypt secret.", parent=self)
                return

            self.clipboard_clear()
            self.clipboard_append(decrypted)

            # Schedule automatic clipboard clearing for security
            self.after(
                self.CLIPBOARD_TIMEOUT_SECONDS * 1000,
                lambda: self.clipboard_clear()
            )

            messagebox.showinfo(
                "Copied to Clipboard",
                f"Secret for '{cred.title}' copied!\nClipboard will automatically clear in 30 seconds for security.",
                parent=self,
            )
        except Exception as exc:
            messagebox.showerror("Decryption Error", f"Failed to decrypt: {exc}", parent=self)

    def _reveal_selected_secret(self) -> None:
        cred = self._get_selected_credential()
        if not cred:
            return

        try:
            decrypted = EncryptionService.decrypt(cred.get_primary_secret(), self.master_password) or ""

            # Popover Dialog to view secret safely
            win = tk.Toplevel(self)
            win.title(f"Secret: {cred.title}")
            win.geometry("420x220")
            win.configure(bg=HexDarkTheme.BG_DARK)
            win.transient(self)

            box = tk.Frame(win, bg=HexDarkTheme.BG_CARD, padx=20, pady=20)
            box.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

            tk.Label(box, text=f"Secret for: {cred.title}", font=HexDarkTheme.FONT_HEADER, fg=HexDarkTheme.ACCENT_GREEN, bg=HexDarkTheme.BG_CARD).pack(anchor="w", pady=(0, 8))
            tk.Label(box, text=cred.get_summary(), font=HexDarkTheme.FONT_SMALL, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w", pady=(0, 10))

            entry = ttk.Entry(box, font=HexDarkTheme.FONT_CODE)
            entry.pack(fill=tk.X, pady=(0, 12))
            entry.insert(0, decrypted)

            btn_frame = tk.Frame(box, bg=HexDarkTheme.BG_CARD)
            btn_frame.pack(fill=tk.X)

            copy_btn = ttk.Button(btn_frame, text="📋 Copy", style="Blue.TButton", command=lambda: [self.clipboard_clear(), self.clipboard_append(decrypted), win.destroy()])
            copy_btn.pack(side=tk.LEFT)

            close_btn = ttk.Button(btn_frame, text="Close", style="Secondary.TButton", command=win.destroy)
            close_btn.pack(side=tk.RIGHT)

        except Exception as exc:
            messagebox.showerror("Error", f"Failed to reveal secret: {exc}", parent=self)

    def _open_generator(self) -> None:
        PasswordGeneratorDialog(self)

    def _run_multithreaded_audit(self) -> None:
        """Spawns background daemon thread to perform audit analysis asynchronously."""
        def on_complete(report: AuditReport) -> None:
            # Deliver callback safely to Tkinter Event Loop
            self.after(0, lambda: SecurityAuditDialog(self, report))

        auditor = SecurityAuditorThread(
            credentials=self.credentials,
            master_password=self.master_password,
            on_complete=on_complete,
        )
        auditor.start()

    def _export_vault(self) -> None:
        """Exports encrypted vault credentials to a JSON file for backup."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Export Encrypted Vault Backup",
            initialfile="securehex_vault_backup.json",
        )
        if not file_path:
            return

        export_data = {
            "version": "2.0.0",
            "owner": self.user.email,
            "items": [],
        }

        for c in self.credentials:
            item_dict = {
                "id": c.id,
                "title": c.title,
                "category": c.category,
                "created_at": c.created_at,
                "last_modified": c.last_modified,
            }
            if isinstance(c, WebCredential):
                item_dict.update({"url": c.url, "username": c.username, "secret": c.encrypted_password})
            elif isinstance(c, CardCredential):
                item_dict.update({
                    "cardholder": c.cardholder_name,
                    "expiry": c.expiry_date,
                    "secret": c.card_number_encrypted,
                    "cvv": c.cvv_encrypted,
                })
            elif isinstance(c, SecureNote):
                item_dict.update({"tags": c.tags, "secret": c.encrypted_note})
            export_data["items"].append(item_dict)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2)
            messagebox.showinfo("Export Successful", f"Vault successfully backed up ({len(self.credentials)} encrypted items)!", parent=self)
        except Exception as exc:
            messagebox.showerror("Export Failed", f"Failed to export: {exc}", parent=self)

    def lock_vault(self) -> None:
        """Locks the vault and invokes parent lock handler."""
        self.auto_lock.stop()
        self.on_lock()

    def logout(self) -> None:
        """Logs out of the application."""
        self.auto_lock.stop()
        self.on_logout()
