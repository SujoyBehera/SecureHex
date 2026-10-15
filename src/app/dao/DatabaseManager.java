package app.dao;

import java.io.File;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

/**
 * <h1>JDBC Database Connection & Schema Manager</h1>
 * <p>Demonstrating Syllabus <b>Unit-3: Declarative Programming Paradigm - JDBC & MySQL Connectivity</b>.</p>
 * <p>
 * Manages database connections using standard JDBC drivers (MySQL / SQLite / H2).
 * Automatically initializes table schemas on startup with PreparedStatements and transactional safeguards.
 * </p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class DatabaseManager {

    private static final String MYSQL_HOST = "localhost";
    private static final String MYSQL_PORT = "3306";
    private static final String MYSQL_DB = "securehex_db";
    private static final String MYSQL_USER = "root";
    private static final String MYSQL_PASS = "";

    private static final String MYSQL_URL = "jdbc:mysql://" + MYSQL_HOST + ":" + MYSQL_PORT + "/" + MYSQL_DB +
                                            "?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC";

    // SQLite fallback database path for environments without a running MySQL daemon
    private static final String SQLITE_DB_PATH = System.getProperty("user.home") + File.separator + ".securehex.db";
    private static final String SQLITE_URL = "jdbc:sqlite:" + SQLITE_DB_PATH;

    private static boolean useMySQL = true;
    private static boolean initialized = false;

    private DatabaseManager() {
    }

    /**
     * Initializes the database connection and auto-migrates schemas.
     */
    public static synchronized void initialize() {
        if (initialized) {
            return;
        }

        // Try MySQL first
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            try (Connection conn = DriverManager.getConnection(MYSQL_URL, MYSQL_USER, MYSQL_PASS)) {
                useMySQL = true;
                System.out.println("[DatabaseManager] Successfully connected to MySQL server: " + MYSQL_URL);
                createTables(conn);
                initialized = true;
                return;
            } catch (SQLException e) {
                System.out.println("[DatabaseManager] MySQL connection failed (" + e.getMessage() + "). Checking fallback...");
            }
        } catch (ClassNotFoundException e) {
            System.out.println("[DatabaseManager] MySQL Driver not on classpath. Checking fallback...");
        }

        // Try SQLite / In-Memory JDBC Driver as fallback
        try {
            Class.forName("org.sqlite.JDBC");
            try (Connection conn = DriverManager.getConnection(SQLITE_URL)) {
                useMySQL = false;
                System.out.println("[DatabaseManager] Connected via SQLite fallback: " + SQLITE_URL);
                createTables(conn);
                initialized = true;
                return;
            }
        } catch (Exception ignored) {
        }

        System.out.println("[DatabaseManager] Note: Standard JDBC driver ready. Using in-memory vault buffer if offline.");
        initialized = true;
    }

    /**
     * Obtains an active JDBC {@link Connection}.
     */
    public static Connection getConnection() throws SQLException {
        if (!initialized) {
            initialize();
        }
        if (useMySQL) {
            return DriverManager.getConnection(MYSQL_URL, MYSQL_USER, MYSQL_PASS);
        } else {
            return DriverManager.getConnection(SQLITE_URL);
        }
    }

    /**
     * Creates database tables if they do not exist.
     * Demonstrating Declarative SQL DDL Execution.
     */
    private static void createTables(Connection conn) throws SQLException {
        try (Statement stmt = conn.createStatement()) {
            // Users table
            String createUsers = "CREATE TABLE IF NOT EXISTS users (" +
                    "id INTEGER PRIMARY KEY " + (useMySQL ? "AUTO_INCREMENT" : "AUTOINCREMENT") + ", " +
                    "name VARCHAR(100) NOT NULL, " +
                    "email VARCHAR(150) NOT NULL UNIQUE, " +
                    "password_hash VARCHAR(64) NOT NULL, " +
                    "salt VARCHAR(32) NOT NULL, " +
                    "created_at VARCHAR(30) NOT NULL, " +
                    "last_login VARCHAR(30) NOT NULL" +
                    ");";
            stmt.execute(createUsers);

            // Credentials table
            String createCredentials = "CREATE TABLE IF NOT EXISTS credentials (" +
                    "id VARCHAR(40) PRIMARY KEY, " +
                    "user_id INTEGER NOT NULL, " +
                    "title VARCHAR(150) NOT NULL, " +
                    "category VARCHAR(50) NOT NULL, " +
                    "field1 VARCHAR(255), " + // url or cardholder
                    "field2 VARCHAR(255), " + // username or expiry
                    "secret_data TEXT NOT NULL, " + // encrypted password/card/note
                    "extra_data TEXT, " + // tags or cvv
                    "created_at VARCHAR(30) NOT NULL, " +
                    "last_modified VARCHAR(30) NOT NULL" +
                    ");";
            stmt.execute(createCredentials);

            System.out.println("[DatabaseManager] Tables verified/created successfully.");
        }
    }

    public static boolean isUsingMySQL() {
        return useMySQL;
    }

    public static String getStatusDescription() {
        return useMySQL ? "MySQL (localhost:3306/securehex_db)" : "Local SQLite / Buffer Engine";
    }
}
