package app.model;

import java.time.LocalDateTime;

/**
 * <h1>Secure Note Entity</h1>
 * <p>Demonstrating Syllabus <b>Unit-2: Inheritance & Polymorphism</b>.</p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class SecureNote extends Credential {
    private static final long serialVersionUID = 1L;

    private String encryptedNote;
    private String tags;

    public SecureNote(String title, String encryptedNote, String tags) {
        super(title, "Secure Note");
        this.encryptedNote = encryptedNote;
        this.tags = tags;
    }

    public SecureNote(String id, String title, String encryptedNote, String tags,
                      LocalDateTime createdAt, LocalDateTime lastModifiedAt) {
        super(id, title, "Secure Note", createdAt, lastModifiedAt);
        this.encryptedNote = encryptedNote;
        this.tags = tags;
    }

    public String getEncryptedNote() {
        return encryptedNote;
    }

    public void setEncryptedNote(String encryptedNote) {
        this.encryptedNote = encryptedNote;
        updateLastModified();
    }

    public String getTags() {
        return tags;
    }

    public void setTags(String tags) {
        this.tags = tags;
        updateLastModified();
    }

    @Override
    public String getSummary() {
        return "Tags: [" + (tags == null || tags.isEmpty() ? "None" : tags) + "]";
    }

    @Override
    public String getMaskedDetails() {
        return "Encrypted Note Content [Hidden] | Tags: " + tags;
    }

    @Override
    public String getPrimarySecret() {
        return encryptedNote;
    }
}
