"""Asynchronous Security Auditor Worker Thread.

Demonstrating Syllabus:
Unit-3: Concurrent Programming Paradigm - Thread classes, asynchronous tasks, and synchronization.
Performs background inspection of the user's vault to identify:
1. Weak passwords (evaluated by formal PasswordDFA state transitions).
2. Reused/duplicate passwords across different websites and services.
3. Compromised/short credentials.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
import threading
from typing import Callable

from securehex.automata.password_dfa import PasswordDFA
from securehex.models.credential import Credential, WebCredential
from securehex.security.encryption import EncryptionService


@dataclass
class AuditIssue:
    """Represents a specific credential security finding."""

    credential_title: str
    issue_type: str  # "WEAK" | "REUSED" | "ERROR"
    severity: str    # "HIGH" | "MEDIUM" | "CRITICAL"
    description: str


@dataclass
class AuditReport:
    """Aggregate security audit results."""

    total_inspected: int
    weak_count: int
    reused_count: int
    health_score: int
    issues: list[AuditIssue] = field(default_factory=list)

    @property
    def is_all_clean(self) -> bool:
        return self.weak_count == 0 and self.reused_count == 0


class SecurityAuditorThread(threading.Thread):
    """Background worker thread evaluating credential health without blocking the GUI."""

    def __init__(
        self,
        credentials: list[Credential],
        master_password: str,
        on_complete: Callable[[AuditReport], None],
    ) -> None:
        super().__init__(name="SecureHex-SecurityAuditor-Worker", daemon=True)
        self.credentials = list(credentials)
        self.master_password = master_password
        self.on_complete = on_complete

    def run(self) -> None:
        """Executes background audit logic."""
        weak_count = 0
        issues: list[AuditIssue] = []
        password_map: dict[str, list[str]] = defaultdict(list)
        total_inspected = 0

        for cred in self.credentials:
            if isinstance(cred, WebCredential):
                total_inspected += 1
                try:
                    decrypted = EncryptionService.decrypt(
                        cred.encrypted_password, self.master_password
                    )
                    if decrypted is None:
                        continue

                    # 1. Automata DFA evaluation
                    dfa_result = PasswordDFA.evaluate(decrypted)
                    if not dfa_result.is_accepted:
                        weak_count += 1
                        feedback_str = "; ".join(dfa_result.feedback) if dfa_result.feedback else "Weak complexity"
                        issues.append(
                            AuditIssue(
                                credential_title=cred.title,
                                issue_type="WEAK",
                                severity="HIGH" if dfa_result.score < 40 else "MEDIUM",
                                description=f"State: {dfa_result.state.state_name} ({dfa_result.score}/100) — {feedback_str}",
                            )
                        )

                    # 2. Track password reuse
                    password_map[decrypted].append(cred.title)

                except Exception as exc:
                    issues.append(
                        AuditIssue(
                            credential_title=cred.title,
                            issue_type="ERROR",
                            severity="CRITICAL",
                            description=f"Decryption failed: {exc}",
                        )
                    )

        # 3. Detect duplicate passwords
        reused_count = 0
        for _pwd, titles in password_map.items():
            if len(titles) > 1:
                reused_count += len(titles)
                services_str = ", ".join(f"'{t}'" for t in titles)
                issues.append(
                    AuditIssue(
                        credential_title="Reused Across Services",
                        issue_type="REUSED",
                        severity="HIGH",
                        description=f"Same password shared across: {services_str}",
                    )
                )

        # Calculate vault health score (0 - 100)
        if total_inspected == 0:
            health_score = 100
        else:
            deductions = (weak_count * 20) + (reused_count * 15)
            health_score = max(10, min(100, 100 - (deductions // max(1, total_inspected))))

        report = AuditReport(
            total_inspected=total_inspected,
            weak_count=weak_count,
            reused_count=reused_count,
            health_score=health_score,
            issues=issues,
        )

        try:
            self.on_complete(report)
        except Exception:
            pass
