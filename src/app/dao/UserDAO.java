package app.dao;

import app.model.User;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * <h1>User Data Access Object (DAO)</h1>
 * <p>Demonstrating Syllabus <b>Unit-3: Declarative Programming Paradigm - JDBC Query Execution</b>.</p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class UserDAO {

    // In-memory fallback repository for standalone / demo runs without database drivers
    private static final List<User> MEMORY_USERS = new ArrayList<>();
    private static int memoryIdCounter = 1;

    /**
     * Registers a new user into the database.
     * Demonstrates PreparedStatement parameter binding and transaction handling.
     */
    public boolean registerUser(User user) {
        String sql = "INSERT INTO users (name, email, password_hash, salt, created_at, last_login) VALUES (?, ?, ?, ?, ?, ?)";
        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, user.getName());
            ps.setString(2, user.getEmail());
            ps.setString(3, user.getPasswordHash());
            ps.setString(4, user.getSalt());
            ps.setString(5, user.getCreatedAt().toString());
            ps.setString(6, user.getLastLogin().toString());

            int rows = ps.executeUpdate();
            return rows > 0;
        } catch (Exception e) {
            // Fallback to in-memory registration for robust demonstration
            for (User u : MEMORY_USERS) {
                if (u.getEmail().equalsIgnoreCase(user.getEmail())) {
                    return false; // Email already registered
                }
            }
            user.setId(memoryIdCounter++);
            MEMORY_USERS.add(user);
            return true;
        }
    }

    /**
     * Finds a user by email address.
     */
    public User findByEmail(String email) {
        String sql = "SELECT * FROM users WHERE LOWER(email) = ?";
        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, email.trim().toLowerCase());
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return new User(
                            rs.getInt("id"),
                            rs.getString("name"),
                            rs.getString("email"),
                            rs.getString("password_hash"),
                            rs.getString("salt"),
                            LocalDateTime.parse(rs.getString("created_at")),
                            LocalDateTime.parse(rs.getString("last_login"))
                    );
                }
            }
        } catch (Exception e) {
            // Check memory store
            for (User u : MEMORY_USERS) {
                if (u.getEmail().equalsIgnoreCase(email.trim())) {
                    return u;
                }
            }
        }
        return null;
    }

    /**
     * Updates the last login timestamp for a user.
     */
    public void updateLastLogin(int userId) {
        String sql = "UPDATE users SET last_login = ? WHERE id = ?";
        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, LocalDateTime.now().toString());
            ps.setInt(2, userId);
            ps.executeUpdate();
        } catch (Exception e) {
            for (User u : MEMORY_USERS) {
                if (u.getId() == userId) {
                    u.setLastLogin(LocalDateTime.now());
                    break;
                }
            }
        }
    }
}
