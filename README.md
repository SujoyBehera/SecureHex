# 🛡️ SecureHex 2.0 (Python GUI & SQLite Edition)
**Enterprise Secure Credential Management System**  
*Course: 21CSC203P – Advanced Programming Practice (APP)*  
*SRM Institute of Science and Technology*  
*Lead Developer: Sujoy Behera*

---

## 📖 1. Project Overview
**SecureHex** is a multi-paradigm, desktop-grade credential and secret management system built with **Python 3**, **Tkinter GUI**, and **SQLite 3**. Designed specifically to demonstrate all core theoretical and practical paradigms covered in the **21CSC203P** syllabus, SecureHex protects sensitive credentials using military-grade authenticated encryption (**AES-256-GCM**), salted master password hashing (**SHA-256**), declarative relational persistence (**SQLite 3**), concurrent background daemon threads, and formal language validation using a **Deterministic Finite Automaton (DFA)**.

---

## 🧩 2. Syllabus Paradigm Mapping (21CSC203P)

| Unit | Syllabus Paradigm | Concrete Implementation in SecureHex |
| :--- | :--- | :--- |
| **Unit 1: Foundations** | Structured Programming & CSPRNG | • Cryptographic random salt generation and Fisher-Yates array shuffling in `PasswordGenerator`<br>• Information-theoretic Shannon Entropy calculation $E = L \times \log_2(R)$<br>• Encrypted JSON vault export/backup |
| **Unit 2: OOP & Modularity** | Abstraction, Encapsulation, Polymorphism, Tagging Interfaces | • `securehex.models.Credential` abstract base class with encapsulated state<br>• Subclass polymorphism with dynamic method dispatch: `WebCredential`, `CardCredential`, `SecureNote`<br>• Tagging/Marker protocol: `Auditable` |
| **Unit 3: Concurrency** | Multithreading, Daemons & Thread Safety | • Background daemon thread `AutoLockManager` tracking user idle time and locking the vault without freezing the UI<br>• Asynchronous `SecurityAuditorThread` inspecting passwords in the background |
| **Unit 3: Declarative DB** | Relational Persistence & SQL Transactions | • Zero-config **SQLite 3** database (`securehex.db`) with Foreign Keys, indexed lookups, and auto-migration<br>• Prepared statements with parameterized query execution preventing SQL Injection<br>• Complete DAO layer: `DatabaseManager`, `UserDAO`, `CredentialDAO` |
| **Unit 3: GUI Paradigm** | Desktop GUI (MVC Architecture) & Event Handling | • Modern Hex-Dark Cyber UI (`HexDarkTheme`) built with **Tkinter** and `ttk`<br>• Dynamic credentials table (`ttk.Treeview`) with search and category filters<br>• Event-driven key/mouse listeners, clipboard auto-clearing after 30 seconds for security |
| **Unit 5: Formal Automata** | Finite Automata (Deterministic Finite Automaton) | • Formal 5-tuple machine $M = (Q, \Sigma, \delta, q_0, F)$ in `PasswordDFA`<br>• Real-time state transitions across $\{Q_{START}, Q_{SHORT}, Q_{WEAK}, Q_{MODERATE}, Q_{STRONG}, Q_{EXCELLENT}\}$<br>• Visual real-time canvas meter in registration and credential dialogs |

---

## 🏗️ 3. Architecture & Directory Structure

```
SecureHex/
├── securehex/                                # Core Python Package
│   ├── automata/                             # Unit 5: Formal Automata Paradigm
│   │   ├── __init__.py
│   │   ├── dfa_state.py                      # DFA State definitions & colors
│   │   └── password_dfa.py                   # 5-tuple DFA state transition machine
│   ├── concurrency/                          # Unit 3: Concurrent Programming
│   │   ├── __init__.py
│   │   ├── autolock.py                       # Daemon inactivity auto-lock thread
│   │   └── security_auditor.py               # Asynchronous vault auditor worker
│   ├── database/                             # Unit 3: Declarative SQLite Persistence
│   │   ├── __init__.py
│   │   ├── db_manager.py                     # SQLite connection manager & DDL
│   │   ├── user_dao.py                       # User entity CRUD operations
│   │   └── credential_dao.py                 # Polymorphic credential CRUD & search
│   ├── gui/                                  # Unit 3: Tkinter Desktop GUI (MVC)
│   │   ├── __init__.py
│   │   ├── theme.py                          # Hex-Dark cybersecurity styling
│   │   ├── password_meter.py                 # Real-time DFA canvas visualizer
│   │   ├── login_frame.py                    # Sign In / Register tabs & attempts limit
│   │   ├── add_dialog.py                     # Polymorphic Add/Edit modal dialog
│   │   ├── generator_dialog.py               # Interactive password generator dialog
│   │   ├── audit_dialog.py                   # Multithreaded security audit report modal
│   │   ├── dashboard_frame.py                # Main vault dashboard & Treeview table
│   │   └── app_window.py                     # Root Tkinter controller & view switcher
│   ├── models/                               # Unit 2: Object-Oriented Domain Hierarchy
│   │   ├── __init__.py
│   │   ├── credential.py                     # Abstract Credential & Auditable protocol
│   │   ├── user.py                           # Encapsulated User model
│   └── security/                             # Cryptography & Generators
│       ├── __init__.py
│       ├── encryption.py                     # AES-256-GCM authenticated encryption
│       ├── hasher.py                         # Salted SHA-256 hashing & constant-time verify
│       └── generator.py                      # Procedural password generator & entropy
├── tests/
│   └── test_securehex.py                     # Automated Pytest suite (13 test cases)
├── main.py                                   # Application Launcher (GUI & CLI fallback)
├── requirements.txt                          # Python dependencies
├── README.md                                 # Technical documentation
└── .gitignore                                # Version control ignore rules
```

---

## 🚀 4. How to Install & Run

### Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- `tkinter` (included with standard Python on Windows/macOS)

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Launch Desktop GUI Application
```powershell
python main.py
```

### 3. Launch Interactive CLI Demonstration / Verification Mode (Optional)
```powershell
python main.py --cli
```

### 4. Run Automated Test Suite
```powershell
python -m pytest tests/test_securehex.py -v
```

---

## 🔒 5. Key Security Specifications

1. **AES-256-GCM Authenticated Encryption:**
   - Confidentiality and integrity verification via Galois/Counter Mode (GCM).
   - Generates unique 12-byte cryptographically secure random Initialization Vectors (IV) per entry.
   - 128-bit authentication tag guarantees tamper detection.

2. **Salted SHA-256 Master Password Hashing:**
   - 16-byte random salt generated via `os.urandom` (CSPRNG).
   - Defeats rainbow table and pre-computation attacks.

3. **Timing-Attack Resistance:**
   - Hash verifications execute in constant time using `hmac.compare_digest` / `MessageDigest.isEqual`.

4. **Inactivity Auto-Lock Daemon:**
   - Dedicated daemon background thread tracks keyboard and mouse activity.
   - Automatically unloads keys and returns to lock screen after inactivity threshold (default: 180 seconds).

5. **Clipboard Sanitization:**
   - Decrypted credentials copied to the system clipboard trigger an automatic wipe timer that securely purges clipboard content after 30 seconds.

6. **SQLite Injection Immunity:**
   - All SQL statements use strictly parameterized queries with prepared statements (`?` parameter binding).

---

## 👥 6. Developer Attribution
- **Sujoy Behera** — Lead Developer & Architect
- SRM Institute of Science and Technology, Kattankulathur
