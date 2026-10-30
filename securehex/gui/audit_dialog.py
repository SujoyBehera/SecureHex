"""Multithreaded Security Audit Results Dialog.

Demonstrating Syllabus:
Unit-3: Concurrency - Thread communication and EDT safe callbacks.
Unit-5: Automata Based Password Analysis presentation.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from securehex.concurrency.security_auditor import AuditReport
from securehex.gui.theme import HexDarkTheme


class SecurityAuditDialog(tk.Toplevel):
    """Displays findings from the multithreaded vault security audit."""

    def __init__(self, parent: tk.Widget, report: AuditReport) -> None:
        super().__init__(parent)
        self.report = report

        self.title("SecureHex — Multithreaded Vault Security Audit")
        self.geometry("640x500")
        self.minsize(580, 440)
        self.configure(bg=HexDarkTheme.BG_DARK)
        self.transient(parent)
        self.grab_set()

        self._build_ui()

    def _build_ui(self) -> None:
        container = tk.Frame(self, bg=HexDarkTheme.BG_CARD, padx=20, pady=18)
        container.pack(fill=tk.BOTH, expand=True, padx=14, pady=14)

        # Header Title
        tk.Label(
            container,
            text="🛡️ Asynchronous Security Auditor Report",
            font=HexDarkTheme.FONT_TITLE,
            fg=HexDarkTheme.ACCENT_GREEN,
            bg=HexDarkTheme.BG_CARD,
        ).pack(anchor="w", pady=(0, 12))

        # Metrics Card Row
        metrics_frame = tk.Frame(container, bg=HexDarkTheme.BG_CARD)
        metrics_frame.pack(fill=tk.X, pady=(0, 14))

        self._create_stat_box(metrics_frame, "Inspected", str(self.report.total_inspected), HexDarkTheme.ACCENT_BLUE)
        self._create_stat_box(metrics_frame, "Weak Passwords", str(self.report.weak_count), HexDarkTheme.ACCENT_RED)
        self._create_stat_box(metrics_frame, "Reused Passwords", str(self.report.reused_count), HexDarkTheme.ACCENT_YELLOW)
        score_color = HexDarkTheme.ACCENT_GREEN if self.report.health_score >= 80 else HexDarkTheme.ACCENT_YELLOW
        self._create_stat_box(metrics_frame, "Vault Health", f"{self.report.health_score}%", score_color)

        # Issues Section Header
        issues_header = "Detected Security Weaknesses & Duplicate Passwords:"
        if self.report.is_all_clean:
            issues_header = "🎉 Excellent hygiene! No weak or reused passwords detected."

        tk.Label(
            container,
            text=issues_header,
            font=HexDarkTheme.FONT_BODY_BOLD,
            fg=HexDarkTheme.TEXT_PRIMARY if not self.report.is_all_clean else HexDarkTheme.ACCENT_GREEN,
            bg=HexDarkTheme.BG_CARD,
        ).pack(anchor="w", pady=(4, 6))

        # Issues Table (Treeview)
        table_frame = tk.Frame(container, bg=HexDarkTheme.BG_CARD)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 12))

        columns = ("type", "target", "description")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        tree.heading("type", text="Severity")
        tree.heading("target", text="Credential / Scope")
        tree.heading("description", text="Audit Finding & Recommendation")

        tree.column("type", width=90, anchor="center")
        tree.column("target", width=180, anchor="w")
        tree.column("description", width=300, anchor="w")

        # Scrollbar
        sb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

        for issue in self.report.issues:
            tree.insert("", tk.END, values=(issue.severity, issue.credential_title, issue.description))

        # Bottom Close Button
        btn_bar = tk.Frame(container, bg=HexDarkTheme.BG_CARD)
        btn_bar.pack(fill=tk.X)
        close_btn = ttk.Button(btn_bar, text="Close Report", style="Secondary.TButton", command=self.destroy)
        close_btn.pack(side=tk.RIGHT)

    def _create_stat_box(self, parent: tk.Widget, title: str, val: str, color: str) -> None:
        box = tk.Frame(parent, bg=HexDarkTheme.BG_INPUT, padx=12, pady=8)
        box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=4)

        tk.Label(box, text=title, font=HexDarkTheme.FONT_SMALL, fg=HexDarkTheme.TEXT_MUTED, bg=HexDarkTheme.BG_INPUT).pack()
        tk.Label(box, text=val, font=HexDarkTheme.FONT_TITLE, fg=color, bg=HexDarkTheme.BG_INPUT).pack()
