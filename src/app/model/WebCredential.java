package app.model;

import java.time.LocalDateTime;

/**
 * <h1>Web Credential Entity</h1>
 * <p>Demonstrating Syllabus <b>Unit-2: Inheritance, Polymorphism, Method Overriding</b>.</p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class WebCredential extends Credential {
    private static final long serialVersionUID = 1L;

    private String url;
    private String username;
    private String encryptedPassword;

    public WebCredential(String title, String url, String username, String encryptedPassword) {
        super(title, "Web Login");
        this.url = url;
        this.username = username;
        this.encryptedPassword = encryptedPassword;
    }

    public WebCredential(String id, String title, String url, String username, String encryptedPassword,
                         LocalDateTime createdAt, LocalDateTime lastModifiedAt) {
        super(id, title, "Web Login", createdAt, lastModifiedAt);
        this.url = url;
        this.username = username;
        this.encryptedPassword = encryptedPassword;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
        updateLastModified();
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
        updateLastModified();
    }

    public String getEncryptedPassword() {
        return encryptedPassword;
    }

    public void setEncryptedPassword(String encryptedPassword) {
        this.encryptedPassword = encryptedPassword;
        updateLastModified();
    }

    // --- Unit-2: Method Overriding (Polymorphic Behavior) ---
    @Override
    public String getSummary() {
        return "User: " + username + " | URL: " + url;
    }

    @Override
    public String getMaskedDetails() {
        return "Username: " + username + " | Password: •••••••• (" + url + ")";
    }

    @Override
    public String getPrimarySecret() {
        return encryptedPassword;
    }
}
