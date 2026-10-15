-- ====================================================================
-- SecureHex: Advanced Programming Practice (APP - 21CSC203P)
-- Database: MySQL Declarative Paradigm Integration
-- ====================================================================

CREATE DATABASE IF NOT EXISTS securehex_db;
USE securehex_db;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(64) NOT NULL,
    salt VARCHAR(32) NOT NULL,
    created_at VARCHAR(30) NOT NULL,
    last_login VARCHAR(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Credentials Table (Polymorphic Entities)
CREATE TABLE IF NOT EXISTS credentials (
    id VARCHAR(40) PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    category VARCHAR(50) NOT NULL,
    field1 VARCHAR(255),               -- URL (Web) or Cardholder (Card)
    field2 VARCHAR(255),               -- Username (Web) or Expiry (Card)
    secret_data TEXT NOT NULL,         -- AES-256 GCM Encrypted Password / Card Number / Note
    extra_data TEXT,                   -- Tags (Note) or CVV (Card)
    created_at VARCHAR(30) NOT NULL,
    last_modified VARCHAR(30) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Indexes for optimal lookup
CREATE INDEX idx_user_credentials ON credentials(user_id);
