package app.model;

import java.io.Serializable;
import java.time.LocalDateTime;

/**
 * <h1>User Account Model</h1>
 * <p>Demonstrating Syllabus <b>Unit-2: Objects and Classes, Encapsulation, Constructors</b>.</p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class User implements Serializable {
    private static final long serialVersionUID = 1L;

    private int id;
    private String name;
    private String email;
    private String passwordHash;
    private String salt;
    private LocalDateTime createdAt;
    private LocalDateTime lastLogin;

    public User(String name, String email, String passwordHash, String salt) {
        this.name = name;
        this.email = email.trim().toLowerCase();
        this.passwordHash = passwordHash;
        this.salt = salt;
        this.createdAt = LocalDateTime.now();
        this.lastLogin = LocalDateTime.now();
    }

    public User(int id, String name, String email, String passwordHash, String salt,
                LocalDateTime createdAt, LocalDateTime lastLogin) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.passwordHash = passwordHash;
        this.salt = salt;
        this.createdAt = createdAt;
        this.lastLogin = lastLogin;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email.trim().toLowerCase();
    }

    public String getPasswordHash() {
        return passwordHash;
    }

    public void setPasswordHash(String passwordHash) {
        this.passwordHash = passwordHash;
    }

    public String getSalt() {
        return salt;
    }

    public void setSalt(String salt) {
        this.salt = salt;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getLastLogin() {
        return lastLogin;
    }

    public void setLastLogin(LocalDateTime lastLogin) {
        this.lastLogin = lastLogin;
    }
}
