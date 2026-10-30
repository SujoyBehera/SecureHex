"""Add and Edit Credential Modal Dialog.

Demonstrating Syllabus:
Unit-2: Polymorphic Entity Instantiation & Encapsulation.
Unit-3: Tkinter GUI Event Handling, Notebook Tabs, Dynamic Field Validation.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from securehex.database.credential_dao import CredentialDAO
from securehex.gui.password_meter import PasswordStrengthMeter
from securehex.gui.theme import HexDarkTheme
from securehex.models.credential import CardCredential, Credential, SecureNote, WebCredential
from securehex.models.user import User
from securehex.security.encryption import EncryptionService
from securehex.security.generator import PasswordGenerator


class AddCredentialDialog(tk.Toplevel):
    """Modal dialog for creating or editing vault items."""

    def __init__(
        self,
        parent: tk.Widget,
        user: User,
        master_password: str,
        credential_dao: CredentialDAO,
        on_saved_callback: Callable[[], None],
        credential_to_edit: Credential | None = None,
    ) -> None:
        super().__init__(parent)
        self.user = user
        self.master_password = master_password
        self.dao = credential_dao
        self.on_saved = on_saved_callback
        self.editing_item = credential_to_edit

        self.title("SecureHex — " + ("Edit Item" if credential_to_edit else "Add New Vault Item"))
        self.geometry("540x620")
        self.minsize(500, 580)
        self.configure(bg=HexDarkTheme.BG_DARK)
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        if self.editing_item:
            self._populate_edit_data()

    def _build_ui(self) -> None:
        container = tk.Frame(self, bg=HexDarkTheme.BG_CARD, padx=24, pady=20)
        container.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        # Header
        header_text = "Edit Vault Item" if self.editing_item else "Add Vault Item"
        header_lbl = tk.Label(
            container,
            text=f"🔐 {header_text}",
            font=HexDarkTheme.FONT_TITLE,
            fg=HexDarkTheme.ACCENT_GREEN,
            bg=HexDarkTheme.BG_CARD,
        )
        header_lbl.pack(anchor="w", pady=(0, 15))

        # Title / Service Name
        tk.Label(
            container,
            text="Title / Service Name:",
            font=HexDarkTheme.FONT_BODY_BOLD,
            fg=HexDarkTheme.TEXT_PRIMARY,
            bg=HexDarkTheme.BG_CARD,
        ).pack(anchor="w")

        self.title_entry = ttk.Entry(container, width=45)
        self.title_entry.pack(fill=tk.X, pady=(4, 12))

        # Category Tabs (Notebook)
        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # 1. Web Login Tab
        self.web_tab = tk.Frame(self.notebook, bg=HexDarkTheme.BG_CARD, padx=12, pady=12)
        self._build_web_tab()
        self.notebook.add(self.web_tab, text="🌐 Web Login")

        # 2. Card Tab
        self.card_tab = tk.Frame(self.notebook, bg=HexDarkTheme.BG_CARD, padx=12, pady=12)
        self._build_card_tab()
        self.notebook.add(self.card_tab, text="💳 Payment Card")

        # 3. Secure Note Tab
        self.note_tab = tk.Frame(self.notebook, bg=HexDarkTheme.BG_CARD, padx=12, pady=12)
        self._build_note_tab()
        self.notebook.add(self.note_tab, text="📝 Secure Note")

        # Bottom Action Bar
        btn_bar = tk.Frame(container, bg=HexDarkTheme.BG_CARD)
        btn_bar.pack(fill=tk.X, pady=(10, 0))

        save_btn = ttk.Button(btn_bar, text="💾 Save Encrypted (AES-256)", style="Accent.TButton", command=self._on_save)
        save_btn.pack(side=tk.RIGHT, padx=(6, 0))

        cancel_btn = ttk.Button(btn_bar, text="Cancel", style="Secondary.TButton", command=self.destroy)
        cancel_btn.pack(side=tk.RIGHT)

    def _build_web_tab(self) -> None:
        tk.Label(self.web_tab, text="Website URL:", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w")
        self.web_url = ttk.Entry(self.web_tab)
        self.web_url.pack(fill=tk.X, pady=(2, 8))

        tk.Label(self.web_tab, text="Username / Email:", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w")
        self.web_username = ttk.Entry(self.web_tab)
        self.web_username.pack(fill=tk.X, pady=(2, 8))

        pwd_header = tk.Frame(self.web_tab, bg=HexDarkTheme.BG_CARD)
        pwd_header.pack(fill=tk.X)
        tk.Label(pwd_header, text="Password:", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(side=tk.LEFT)

        gen_btn = ttk.Button(pwd_header, text="⚡ Generate Strong", style="Blue.TButton", command=self._generate_web_pwd)
        gen_btn.pack(side=tk.RIGHT)

        self.web_pwd = ttk.Entry(self.web_tab, show="•")
        self.web_pwd.pack(fill=tk.X, pady=(2, 6))

        # Real-time DFA password meter
        self.web_meter = PasswordStrengthMeter(self.web_tab)
        self.web_meter.pack(fill=tk.X, pady=(2, 0))
        self.web_pwd.bind("<KeyRelease>", lambda e: self.web_meter.update_strength(self.web_pwd.get()))

    def _build_card_tab(self) -> None:
        tk.Label(self.card_tab, text="Cardholder Name:", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w")
        self.card_name = ttk.Entry(self.card_tab)
        self.card_name.pack(fill=tk.X, pady=(2, 8))

        tk.Label(self.card_tab, text="Card Number (Encrypted):", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w")
        self.card_num = ttk.Entry(self.card_tab)
        self.card_num.pack(fill=tk.X, pady=(2, 8))

        row2 = tk.Frame(self.card_tab, bg=HexDarkTheme.BG_CARD)
        row2.pack(fill=tk.X, pady=(0, 8))

        col1 = tk.Frame(row2, bg=HexDarkTheme.BG_CARD)
        col1.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))
        tk.Label(col1, text="Expiry (MM/YY):", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w")
        self.card_expiry = ttk.Entry(col1)
        self.card_expiry.pack(fill=tk.X, pady=(2, 0))

        col2 = tk.Frame(row2, bg=HexDarkTheme.BG_CARD)
        col2.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(6, 0))
        tk.Label(col2, text="CVV / CVC (Encrypted):", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w")
        self.card_cvv = ttk.Entry(col2, show="•")
        self.card_cvv.pack(fill=tk.X, pady=(2, 0))

    def _build_note_tab(self) -> None:
        tk.Label(self.note_tab, text="Tags (comma separated):", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w")
        self.note_tags = ttk.Entry(self.note_tab)
        self.note_tags.pack(fill=tk.X, pady=(2, 8))

        tk.Label(self.note_tab, text="Encrypted Note Secret Content:", font=HexDarkTheme.FONT_BODY, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_CARD).pack(anchor="w")
        self.note_text = tk.Text(
            self.note_tab,
            height=7,
            bg=HexDarkTheme.BG_INPUT,
            fg=HexDarkTheme.TEXT_PRIMARY,
            insertbackground=HexDarkTheme.TEXT_PRIMARY,
            bd=0,
            padx=8,
            pady=8,
            font=HexDarkTheme.FONT_BODY,
        )
        self.note_text.pack(fill=tk.BOTH, expand=True, pady=(2, 0))

    def _generate_web_pwd(self) -> None:
        pwd = PasswordGenerator.generate_default()
        self.web_pwd.delete(0, tk.END)
        self.web_pwd.insert(0, pwd)
        self.web_meter.update_strength(pwd)

    def _populate_edit_data(self) -> None:
        item = self.editing_item
        if not item:
            return
        self.title_entry.insert(0, item.title)

        if isinstance(item, WebCredential):
            self.notebook.select(0)
            self.web_url.insert(0, item.url)
            self.web_username.insert(0, item.username)
            decrypted = EncryptionService.decrypt(item.encrypted_password, self.master_password) or ""
            self.web_pwd.insert(0, decrypted)
            self.web_meter.update_strength(decrypted)
        elif isinstance(item, CardCredential):
            self.notebook.select(1)
            self.card_name.insert(0, item.cardholder_name)
            decrypted_num = EncryptionService.decrypt(item.card_number_encrypted, self.master_password) or ""
            self.card_num.insert(0, decrypted_num)
            self.card_expiry.insert(0, item.expiry_date)
            decrypted_cvv = EncryptionService.decrypt(item.cvv_encrypted, self.master_password) or ""
            self.card_cvv.insert(0, decrypted_cvv)
        elif isinstance(item, SecureNote):
            self.notebook.select(2)
            self.note_tags.insert(0, item.tags)
            decrypted_note = EncryptionService.decrypt(item.encrypted_note, self.master_password) or ""
            self.note_text.insert("1.0", decrypted_note)

    def _on_save(self) -> None:
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Validation Error", "Title / Service Name is required.", parent=self)
            return

        current_tab_idx = self.notebook.index(self.notebook.select())
        item_id = self.editing_item.id if self.editing_item else None
        created_at = self.editing_item.created_at if self.editing_item else None

        try:
            if current_tab_idx == 0:  # Web Login
                pwd = self.web_pwd.get()
                if not pwd:
                    messagebox.showerror("Validation Error", "Password cannot be empty.", parent=self)
                    return
                enc_pwd = EncryptionService.encrypt(pwd, self.master_password)
                credential = WebCredential(
                    title=title,
                    url=self.web_url.get().strip(),
                    username=self.web_username.get().strip(),
                    encrypted_password=enc_pwd or "",
                    item_id=item_id,
                    user_id=self.user.id,
                    created_at=created_at,
                )
            elif current_tab_idx == 1:  # Card
                card_no = self.card_num.get().strip()
                if not card_no:
                    messagebox.showerror("Validation Error", "Card Number is required.", parent=self)
                    return
                enc_num = EncryptionService.encrypt(card_no, self.master_password)
                enc_cvv = EncryptionService.encrypt(self.card_cvv.get().strip(), self.master_password)
                credential = CardCredential(
                    title=title,
                    cardholder_name=self.card_name.get().strip(),
                    card_number_encrypted=enc_num or "",
                    expiry_date=self.card_expiry.get().strip(),
                    cvv_encrypted=enc_cvv or "",
                    item_id=item_id,
                    user_id=self.user.id,
                    created_at=created_at,
                )
            else:  # Secure Note
                content = self.note_text.get("1.0", tk.END).strip()
                if not content:
                    messagebox.showerror("Validation Error", "Note content cannot be empty.", parent=self)
                    return
                enc_note = EncryptionService.encrypt(content, self.master_password)
                credential = SecureNote(
                    title=title,
                    encrypted_note=enc_note or "",
                    tags=self.note_tags.get().strip(),
                    item_id=item_id,
                    user_id=self.user.id,
                    created_at=created_at,
                )

            # Persist via CredentialDAO into SQLite
            self.dao.save(self.user.id, credential)
            self.on_saved()
            self.destroy()

        except Exception as exc:
            messagebox.showerror("Encryption / Save Error", f"Failed to save credential: {exc}", parent=self)
