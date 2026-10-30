"""Automated unit test suite verifying all SecureHex components:
- Cryptographic Engine (AES-256-GCM, Salted SHA-256)
- Password DFA Automaton State Machine
- Password Generator & Entropy
- SQLite Relational Persistence (UserDAO & CredentialDAO)
- AutoLock & Concurrency
"""

from __future__ import annotations

import os
import tempfile
import time
import pytest

from securehex.automata.dfa_state import DFAState
from securehex.automata.password_dfa import PasswordDFA
from securehex.concurrency.autolock import AutoLockManager
from securehex.concurrency.security_auditor import SecurityAuditorThread
from securehex.database.credential_dao import CredentialDAO
from securehex.database.db_manager import DatabaseManager
from securehex.database.user_dao import UserDAO
from securehex.models.credential import CardCredential, SecureNote, WebCredential
from securehex.security.encryption import EncryptionService
from securehex.security.generator import PasswordGenerator
from securehex.security.hasher import PasswordHasher


@pytest.fixture
def temp_db():
    """Provides a fresh temporary SQLite database for test isolation."""
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    DatabaseManager.set_db_path(path)
    DatabaseManager.initialize()
    yield path
    try:
        os.remove(path)
    except OSError:
        pass


class TestSecurity:
    """Verifies cryptographic algorithms and CSPRNG behavior."""

    def test_hasher_matches_and_rejects_wrong_password(self):
        salt = PasswordHasher.generate_salt()
        pwd = "SRM_Computer_Science_2026!"
        hashed = PasswordHasher.hash_password(pwd, salt)

        assert PasswordHasher.verify_password(pwd, hashed, salt) is True
        assert PasswordHasher.verify_password("wrong_password", hashed, salt) is False
        assert PasswordHasher.verify_password("", hashed, salt) is False

    def test_aes_256_gcm_encrypt_decrypt_integrity(self):
        plain = "Confidential_API_Secret_Key_XYZ987654"
        master = "MasterKey@123"

        encrypted = EncryptionService.encrypt(plain, master)
        assert encrypted is not None
        assert encrypted != plain

        decrypted = EncryptionService.decrypt(encrypted, master)
        assert decrypted == plain

    def test_aes_decrypt_fails_with_wrong_key(self):
        plain = "TopSecretInformation"
        encrypted = EncryptionService.encrypt(plain, "CorrectKey123")

        with pytest.raises(ValueError):
            EncryptionService.decrypt(encrypted, "WrongKey456")

    def test_password_generator_entropy_and_diversity(self):
        pwd = PasswordGenerator.generate(length=20, use_lower=True, use_upper=True, use_digits=True, use_special=True)
        assert len(pwd) == 20
        assert any(c.islower() for c in pwd)
        assert any(c.isupper() for c in pwd)
        assert any(c.isdigit() for c in pwd)
        assert any(not c.isalnum() for c in pwd)

        entropy = PasswordGenerator.calculate_entropy(pwd)
        assert entropy >= 100.0  # High entropy requirement


class TestAutomataDFA:
    """Verifies Unit-5 Deterministic Finite Automaton (DFA) transitions."""

    def test_empty_password_transition(self):
        res = PasswordDFA.evaluate("")
        assert res.state == DFAState.Q_START
        assert res.score == 0
        assert res.is_accepted is False

    def test_short_password_transition(self):
        res = PasswordDFA.evaluate("Ab1!")
        assert res.state == DFAState.Q_SHORT
        assert res.is_accepted is False

    def test_weak_password_transition(self):
        res = PasswordDFA.evaluate("lowercaseonlyhere")
        assert res.state == DFAState.Q_WEAK
        assert res.is_accepted is False

    def test_moderate_password_transition(self):
        res = PasswordDFA.evaluate("Pass12345")
        assert res.state == DFAState.Q_MODERATE
        assert res.is_accepted is True

    def test_strong_and_excellent_transitions(self):
        strong = PasswordDFA.evaluate("Str0ng!Passw0rd")
        assert strong.state == DFAState.Q_STRONG
        assert strong.is_accepted is True

        excellent = PasswordDFA.evaluate("EnterpriseGrade#Security2026!!")
        assert excellent.state == DFAState.Q_EXCELLENT
        assert excellent.score == 100
        assert excellent.is_accepted is True


class TestDatabaseDAO:
    """Verifies SQLite persistence, polymorphism, and relational integrity."""

    def test_user_creation_and_lookup(self, temp_db):
        user_dao = UserDAO()
        salt = PasswordHasher.generate_salt()
        h = PasswordHasher.hash_password("Pass@123", salt)

        user = user_dao.create_user("Sujoy Behera", "sujoy@srmist.edu.in", h, salt)
        assert user is not None
        assert user.id is not None
        assert user.email == "sujoy@srmist.edu.in"

        # Unique constraint test
        duplicate = user_dao.create_user("Another Name", "sujoy@srmist.edu.in", h, salt)
        assert duplicate is None

        found = user_dao.find_by_email("sujoy@srmist.edu.in")
        assert found is not None
        assert found.id == user.id

    def test_polymorphic_credential_crud(self, temp_db):
        user_dao = UserDAO()
        cred_dao = CredentialDAO()

        salt = PasswordHasher.generate_salt()
        h = PasswordHasher.hash_password("Pass@123", salt)
        user = user_dao.create_user("Test User", "test@example.com", h, salt)

        # 1. Web Credential
        web = WebCredential("GitHub", "https://github.com", "sujoy", "enc_gh_pwd")
        cred_dao.save(user.id, web)

        # 2. Card Credential
        card = CardCredential("HDFC Debit", "Sujoy Behera", "enc_card_no", "12/28", "enc_cvv")
        cred_dao.save(user.id, card)

        # 3. Secure Note
        note = SecureNote("Server SSH Keys", "enc_ssh_body", tags="devops,srm")
        cred_dao.save(user.id, note)

        # Retrieve and verify polymorphism
        items = cred_dao.find_by_user_id(user.id)
        assert len(items) == 3

        types = {type(item) for item in items}
        assert WebCredential in types
        assert CardCredential in types
        assert SecureNote in types

        # Search test
        search_res = cred_dao.search(user.id, "GitHub")
        assert len(search_res) == 1
        assert search_res[0].title == "GitHub"

        # Delete test
        cred_dao.delete(web.id, user.id)
        remaining = cred_dao.find_by_user_id(user.id)
        assert len(remaining) == 2


class TestConcurrency:
    """Verifies Unit-3 Concurrency AutoLock and Multithreaded Auditor."""

    def test_autolock_manager_countdown_and_trigger(self):
        triggered = []

        def callback():
            triggered.append(True)

        mgr = AutoLockManager(timeout_seconds=1, lock_callback=callback)
        mgr.start()
        time.sleep(1.4)
        mgr.stop()

        assert len(triggered) >= 1

    def test_security_auditor_worker_thread(self):
        master = "MasterKey@123"
        enc_weak = EncryptionService.encrypt("weak", master)
        enc_strong = EncryptionService.encrypt("Str0ng#EnterpriseP@ssword2026", master)

        cred1 = WebCredential("Site A", "https://a.com", "user", enc_weak)
        cred2 = WebCredential("Site B", "https://b.com", "user", enc_weak)  # Reuse weak
        cred3 = WebCredential("Site C", "https://c.com", "user", enc_strong)

        report_holder = []

        def on_complete(rep):
            report_holder.append(rep)

        auditor = SecurityAuditorThread([cred1, cred2, cred3], master, on_complete)
        auditor.start()
        auditor.join(timeout=3.0)

        assert len(report_holder) == 1
        rep = report_holder[0]
        assert rep.total_inspected == 3
        assert rep.weak_count >= 1
        assert rep.reused_count >= 2
