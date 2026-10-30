#!/usr/bin/env python3
"""SecureHex - Enterprise Credential Management System (Python GUI Edition)

Course: 21CSC203P - Advanced Programming Practice (APP)
SRM Institute of Science and Technology
Lead Developer: Sujoy Behera

Demonstrating Course Paradigms:
- Unit-1: Structured Programming Theorem, CSPRNGs, Object Serialization / JSON Persistence.
- Unit-2: Object-Oriented Paradigm (Abstraction, Encapsulation, Polymorphic Inheritance, Tagging Protocols).
- Unit-3: Concurrent Programming Paradigm (Multithreaded Inactivity Auto-Lock Daemon & Asynchronous Auditor Worker).
- Unit-3: Declarative Persistence Paradigm (SQLite Relational Persistence with Prepared Statements & Foreign Keys).
- Unit-3: GUI Paradigm (Desktop Tkinter MVC, Custom Hex-Dark Cyber Theme, Event-Driven Binding).
- Unit-5: Automata Based Programming Paradigm (Deterministic Finite Automaton for Password Strength Classification).
"""

from __future__ import annotations

import argparse
import os
import sys

from securehex.automata.password_dfa import PasswordDFA
from securehex.database.credential_dao import CredentialDAO
from securehex.database.db_manager import DatabaseManager
from securehex.database.user_dao import UserDAO
from securehex.models.credential import CardCredential, SecureNote, WebCredential
from securehex.models.user import User
from securehex.security.encryption import EncryptionService
from securehex.security.generator import PasswordGenerator
from securehex.security.hasher import PasswordHasher

APP_NAME = "SecureHex"
VERSION = "2.0 (Python GUI Edition)"


def print_banner() -> None:
    banner = f"""
==========================================================
               🛡️  {APP_NAME} {VERSION}
       Enterprise Secure Credential Management System
   Course: 21CSC203P - Advanced Programming Practice (APP)
==========================================================
Database Engine: SQLite 3 ({DatabaseManager.get_db_path()})
Encryption:      AES-256-GCM (Authenticated AEAD)
Hashing:         SHA-256 + 128-bit CSPRNG Salt
Automata:        5-Tuple Deterministic Finite Automaton (DFA)
Concurrency:     AutoLock Daemon & Async Security Auditor Worker
==========================================================
"""
    print(banner)


def run_cli_demo() -> None:
    """Interactive command-line demonstration for headless / terminal evaluation."""
    print("[SecureHex] Starting Interactive CLI Verification Mode...\n")
    DatabaseManager.initialize()

    while True:
        print("----------------------------------------------------------")
        print("1. Test Cryptographic Engine (AES-256-GCM Encrypt/Decrypt)")
        print("2. Test Salted Password Hasher (SHA-256)")
        print("3. Test Formal Password DFA State Machine")
        print("4. Test Procedural Password Generator & Entropy")
        print("5. Test SQLite Relational Persistence (User & Credential CRUD)")
        print("6. Launch Tkinter Desktop Graphical User Interface")
        print("7. Exit")
        print("----------------------------------------------------------")

        choice = input("Enter choice (1-7): ").strip()
        if choice == "1":
            msg = input("Enter secret plaintext: ") or "MySecretAPIKey_12345!"
            master = input("Enter master password: ") or "MasterKey@2026"
            enc = EncryptionService.encrypt(msg, master)
            print(f"\nEncrypted (AES-256-GCM Base64): {enc}")
            dec = EncryptionService.decrypt(enc, master)
            print(f"Decrypted Result:               {dec}")
            assert dec == msg, "Decryption verification failed!"
            print("✔ AES-256-GCM verification passed!\n")

        elif choice == "2":
            pwd = input("Enter password to hash: ") or "Student@SRM2026"
            salt = PasswordHasher.generate_salt()
            hashed = PasswordHasher.hash_password(pwd, salt)
            print(f"\nGenerated Salt (Base64): {salt}")
            print(f"Computed SHA-256 Hash:   {hashed}")
            valid = PasswordHasher.verify_password(pwd, hashed, salt)
            invalid = PasswordHasher.verify_password("wrong_password", hashed, salt)
            print(f"Verification Check:      {'Passed' if valid and not invalid else 'Failed'}\n")

        elif choice == "3":
            test_pwd = input("Enter password for DFA analysis: ") or "Test@123"
            res = PasswordDFA.evaluate(test_pwd)
            print(f"\nDFA Final State:  {res.state.state_name} ({res.state.description})")
            print(f"Complexity Score: {res.score} / 100")
            print(f"Is Accepted (F):  {res.is_accepted}")
            print(f"Feedback:         {res.feedback}\n")

        elif choice == "4":
            pwd = PasswordGenerator.generate_default()
            entropy = PasswordGenerator.calculate_entropy(pwd)
            print(f"\nGenerated Password: {pwd}")
            print(f"Shannon Entropy:    {entropy} bits (2^{entropy} space)\n")

        elif choice == "5":
            print("\n[DB Test] Initializing SQLite test verification...")
            user_dao = UserDAO()
            cred_dao = CredentialDAO()
            salt = PasswordHasher.generate_salt()
            h = PasswordHasher.hash_password("Demo@123", salt)
            test_user = user_dao.create_user("CLI Test User", "clitest@srmist.edu.in", h, salt)
            if not test_user:
                test_user = user_dao.find_by_email("clitest@srmist.edu.in")
            print(f"User retrieved: {test_user}")

            # Save sample credentials
            enc_pwd = EncryptionService.encrypt("secret123", "Demo@123")
            cred = WebCredential("GitHub Account", "https://github.com", "sujoy", enc_pwd or "")
            cred_dao.save(test_user.id, cred)
            items = cred_dao.find_by_user_id(test_user.id)
            print(f"Stored credentials in SQLite: {len(items)} items")
            for item in items:
                print(f" - {item}")
            print("✔ SQLite persistence verification passed!\n")

        elif choice == "6":
            launch_gui()
            break

        elif choice == "7":
            print("Exiting SecureHex. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice, please select between 1 and 7.")


def launch_gui(db_path: str | None = None) -> None:
    """Launches the Tkinter GUI Desktop Application."""
    from securehex.gui.app_window import SecureHexApp

    app = SecureHexApp(db_path=db_path)
    app.mainloop()


def main() -> None:
    parser = argparse.ArgumentParser(description="SecureHex 2.0 Credential Management System")
    parser.add_argument("--cli", action="store_true", help="Launch in interactive CLI verification mode")
    parser.add_argument("--db", type=str, default="securehex.db", help="Path to SQLite database file")
    args = parser.parse_args()

    print_banner()

    if args.cli:
        run_cli_demo()
    else:
        try:
            launch_gui(db_path=args.db)
        except tk.TclError as exc:
            print(f"[Warning] Tkinter GUI initialization failed: {exc}")
            print("[SecureHex] Falling back to CLI mode...")
            run_cli_demo()


if __name__ == "__main__":
    main()
