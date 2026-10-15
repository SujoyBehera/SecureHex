# 🛡️ SecureHex 2.0 (APP Edition)
**Enterprise Secure Credential Management System**  
*Developed for 21CSC203P – Advanced Programming Practice (Professional Core)*  
*SRM Institute of Science and Technology*

---

## 📖 1. Project Overview
**SecureHex** is a multi-paradigm, desktop-grade credential and secret management system built in Java. Designed specifically to demonstrate all theoretical and practical paradigms covered in the **21CSC203P** syllabus, SecureHex protects sensitive credentials using military-grade authenticated encryption (**AES-256-GCM**), salted password hashing (**SHA-256**), declarative relational persistence (**JDBC/MySQL**), concurrent background worker threads, and formal language validation using a **Deterministic Finite Automaton (DFA)**.

---

## 👥 2. Team Member Distribution (Group of 3)

| Team Member | Project Role | Modules Owned & Paradigms Demonstrated |
| :--- | :--- | :--- |
| **Member 1 (Sujoy Behera - Lead)** | **Core Domain & Security Lead** | • OOP Class Hierarchy (`Credential`, `WebCredential`, `CardCredential`, `SecureNote`)<br>• Tagging Interface (`Auditable`) & Object Serialization (`Serializable`)<br>• Cryptographic Engine (`EncryptionService` AES-256-GCM, `PasswordHasher` SHA-256) |
| **Member 2** | **Concurrency & Database Lead** | • Declarative JDBC Persistence (`DatabaseManager`, `UserDAO`, `CredentialDAO`)<br>• MySQL Schema DDL (`schema.sql`) and `PreparedStatement` query execution<br>• Multithreading: Daemon Inactivity Auto-Lock Thread (`AutoLockManager`) |
| **Member 3** | **Swing GUI & Automata Lead** | • Swing MVC GUI (`LoginRegisterFrame`, `DashboardFrame`, `AddCredentialDialog`, `HexDarkTheme`)<br>• Event-Driven Programming (`AWTEventListener`, `DocumentListener`)<br>• Formal Language Automata: Deterministic Finite Automaton (`PasswordDFA`, `DFAState`) |

---

## 🧩 3. Syllabus Paradigm Mapping (21CSC203P)

| Unit | Syllabus Concept | Concrete Implementation in SecureHex |
| :--- | :--- | :--- |
| **Unit 1: Foundations** | Structured Programming & Object Serialization | • Bohm-Jacopini sequence/selection/iteration constructs in `PasswordGenerator`<br>• `java.io.Serializable` on `Credential` and `User` models for secure binary backup<br>• Dynamic memory allocation and safe array zeroing |
| **Unit 2: Java OOP** | Abstraction, Encapsulation, Inheritance, Polymorphism, Tagging Interfaces | • `app.model.Credential` abstract class with encapsulated private members<br>• Subclass inheritance with dynamic method dispatch (`getSummary()`, `getMaskedDetails()`)<br>• Tagging (Marker) Interface: `app.model.Auditable` |
| **Unit 3: Advanced Java** | Concurrent Programming (Multithreading) & Declarative JDBC | • **Concurrency:** Background daemon thread `AutoLockManager` monitoring user inactivity and asynchronous `SecurityAuditorThread`<br>• **Declarative DB:** `DatabaseManager`, `UserDAO`, `CredentialDAO` executing SQL queries via JDBC with MySQL support and zero-config fallback |
| **Unit 3: GUI Paradigm** | Java Swing (MVC Architecture) & Event Handling | • Clean Model-View-Controller separation<br>• Modern Hex Dark UI (`HexDarkTheme`) with `JTable`, `CardLayout`, custom dialogs, and real-time password strength rendering |
| **Unit 5: Formal Automata** | Finite Automata (DFA State Machine) | • Formal 5-tuple machine $M = (Q, \Sigma, \delta, q_0, F)$ in `PasswordDFA`<br>• Real-time state transitions across $\{Q_{START}, Q_{SHORT}, Q_{WEAK}, Q_{MODERATE}, Q_{STRONG}, Q_{EXCELLENT}\}$ |

---

## 🏗️ 4. Package Structure

```
SecureHex/
├── db/
│   └── schema.sql                             # MySQL Database DDL script
├── src/
│   └── app/
│       ├── Main.java                          # Main entry point & launcher
│       ├── model/                             # Unit 2: OOP & Interfaces
│       │   ├── Auditable.java                 # Tagging/Marker interface
│       │   ├── Credential.java                # Abstract base class (Serializable)
│       │   ├── WebCredential.java             # Subclass (Polymorphism & Overriding)
│       │   ├── CardCredential.java            # Subclass
│       │   ├── SecureNote.java                # Subclass
│       │   └── User.java                      # Encapsulated user entity
│       ├── security/                          # Cryptography & Procedural Generators
│       │   ├── EncryptionService.java         # AES-256-GCM Authenticated Encryption
│       │   ├── PasswordHasher.java            # Salted SHA-256 Hashing
│       │   └── PasswordGenerator.java         # Secure procedural password generator
│       ├── automata/                          # Unit 5: Formal Automata Paradigm
│       │   ├── DFAState.java                  # Finite state enumeration
│       │   └── PasswordDFA.java               # Formal DFA State Machine
│       ├── dao/                               # Unit 3: Declarative JDBC Paradigm
│       │   ├── DatabaseManager.java           # JDBC Connection & Schema Auto-migration
│       │   ├── UserDAO.java                   # User CRUD & PreparedStatement queries
│       │   └── CredentialDAO.java             # Credential CRUD & Transaction logic
│       ├── concurrency/                       # Unit 3: Concurrent Programming
│       │   ├── AutoLockManager.java           # Daemon Inactivity Monitoring Thread
│       │   └── SecurityAuditorThread.java     # Asynchronous Vault Auditor Thread
│       └── gui/                               # Unit 3: Java Swing GUI (MVC)
│           ├── HexDarkTheme.java              # Dark cybersecurity styling & widgets
│           ├── PasswordStrengthBar.java       # DFA-driven dynamic visualizer
│           ├── LoginRegisterFrame.java        # Authentication & Registration view
│           ├── AddCredentialDialog.java       # Polymorphic credential dialog
│           └── DashboardFrame.java            # Main vault dashboard & table
├── README.md
└── SecureHex.iml
```

---

## 🚀 5. How to Build & Run

### Option A: Using IntelliJ IDEA (Recommended)
1. Open IntelliJ IDEA.
2. Click **Open** and select the `SecureHex` folder.
3. Open `src/app/Main.java`.
4. Click the green **Run (▶)** button.

### Option B: Using Command Line (PowerShell / Terminal)
```powershell
# Compile all packages
javac -d bin (Get-ChildItem -Path src -Filter *.java -Recurse).FullName

# Run the Swing GUI Desktop Application
java -cp bin app.Main

# Or run in interactive CLI demonstration mode
java -cp bin app.Main --cli
```

### Option C: Database Setup (Optional)
By default, SecureHex runs with an automatic local fallback engine so it works immediately out of the box without any setup. To connect to an external **MySQL** database:
1. Start your local MySQL service (e.g., via XAMPP or MySQL Workbench).
2. Run the script located at `db/schema.sql`:
   ```sql
   mysql -u root -p < db/schema.sql
   ```
3. SecureHex will automatically detect MySQL on `localhost:3306` and route all persistence queries to it!

---

## 🔒 6. Security Features
- **AES-256 GCM Authenticated Encryption:** Ensures confidentiality and tamper detection using 128-bit authentication tags and unique 12-byte initialization vectors (IV).
- **Salted SHA-256 Master Password Hashing:** Protects master passwords against rainbow table lookups using cryptographically random salts (`SecureRandom`).
- **Timing Attack Resistance:** Implements constant-time hash comparisons (`MessageDigest.isEqual`).
- **Inactivity Auto-Lock:** Background daemon thread automatically closes and locks the vault after 3 minutes of idle time.
- **Lockout Protection:** Enforces a 3-attempt limit on failed authentications to thwart brute-force password guessing.
