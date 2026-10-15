package app.model;

import java.io.Serializable;
import java.time.LocalDateTime;
import java.util.UUID;

/**
 * <h1>Abstract Credential Entity</h1>
 * <p>Demonstrating Syllabus:
 * <ul>
 *   <li><b>Unit-1:</b> Object Serialization (implements {@link Serializable})</li>
 *   <li><b>Unit-2:</b> Abstraction, Encapsulation, Tagging Interface (implements {@link Auditable})</li>
 * </ul>
 * </p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public abstract class Credential implements Serializable, Auditable {
    private static final long serialVersionUID = 1L;

    // Encapsulated fields (Unit-2: Encapsulation - private state with accessors)
    private final String id;
    private String title;
    private String category;
    private LocalDateTime createdAt;
    private LocalDateTime lastModifiedAt;

    /**
     * Default parameterized constructor.
     * Demonstrating Unit-2: Constructor & Data types.
     */
    public Credential(String title, String category) {
        this.id = UUID.randomUUID().toString();
        this.title = title;
        this.category = category;
        this.createdAt = LocalDateTime.now();
        this.lastModifiedAt = LocalDateTime.now();
    }

    /**
     * Overloaded constructor for database reconstitution.
     */
    public Credential(String id, String title, String category, LocalDateTime createdAt, LocalDateTime lastModifiedAt) {
        this.id = id;
        this.title = title;
        this.category = category;
        this.createdAt = createdAt;
        this.lastModifiedAt = lastModifiedAt;
    }

    // --- Unit-2: Abstraction & Polymorphism (Abstract Methods) ---
    public abstract String getSummary();
    public abstract String getMaskedDetails();
    public abstract String getPrimarySecret();

    // --- Getters & Setters (Encapsulation) ---
    public String getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
        this.lastModifiedAt = LocalDateTime.now();
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
        this.lastModifiedAt = LocalDateTime.now();
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public LocalDateTime getLastModifiedAt() {
        return lastModifiedAt;
    }

    public void updateLastModified() {
        this.lastModifiedAt = LocalDateTime.now();
    }

    @Override
    public String toString() {
        return "[" + category + "] " + title + " (ID: " + id.substring(0, 8) + "...)";
    }
}
