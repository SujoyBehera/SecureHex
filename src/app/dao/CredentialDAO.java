package app.dao;

import app.model.CardCredential;
import app.model.Credential;
import app.model.SecureNote;
import app.model.WebCredential;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

/**
 * <h1>Credential Data Access Object (DAO)</h1>
 * <p>Demonstrating Syllabus:
 * <ul>
 *   <li><b>Unit-2:</b> Polymorphism & Dynamic Dispatch (Handling {@link Credential} hierarchy)</li>
 *   <li><b>Unit-3:</b> Declarative Programming Paradigm - JDBC Connectivity with MySQL & Query Execution</li>
 * </ul>
 * </p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class CredentialDAO {

    private static final List<StoredItem> MEMORY_CREDENTIALS = new ArrayList<>();

    private static class StoredItem {
        final int userId;
        final Credential credential;

        StoredItem(int userId, Credential credential) {
            this.userId = userId;
            this.credential = credential;
        }
    }

    /**
     * Saves or inserts a new polymorphic credential into the database.
     */
    public boolean saveCredential(int userId, Credential cred) {
        String sql = "INSERT INTO credentials (id, user_id, title, category, field1, field2, secret_data, extra_data, created_at, last_modified) " +
                     "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

        String field1 = "";
        String field2 = "";
        String secretData = "";
        String extraData = "";

        // Extract polymorphic fields based on runtime type
        if (cred instanceof WebCredential) {
            WebCredential wc = (WebCredential) cred;
            field1 = wc.getUrl();
            field2 = wc.getUsername();
            secretData = wc.getEncryptedPassword();
        } else if (cred instanceof CardCredential) {
            CardCredential cc = (CardCredential) cred;
            field1 = cc.getCardholderName();
            field2 = cc.getExpiryDate();
            secretData = cc.getCardNumberEncrypted();
            extraData = cc.getCvvEncrypted();
        } else if (cred instanceof SecureNote) {
            SecureNote sn = (SecureNote) cred;
            secretData = sn.getEncryptedNote();
            extraData = sn.getTags();
        }

        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, cred.getId());
            ps.setInt(2, userId);
            ps.setString(3, cred.getTitle());
            ps.setString(4, cred.getCategory());
            ps.setString(5, field1);
            ps.setString(6, field2);
            ps.setString(7, secretData);
            ps.setString(8, extraData);
            ps.setString(9, cred.getCreatedAt().toString());
            ps.setString(10, cred.getLastModifiedAt().toString());

            return ps.executeUpdate() > 0;
        } catch (Exception e) {
            // Memory store fallback
            MEMORY_CREDENTIALS.removeIf(item -> item.credential.getId().equals(cred.getId()));
            MEMORY_CREDENTIALS.add(new StoredItem(userId, cred));
            return true;
        }
    }

    /**
     * Retrieves all credentials owned by the user.
     * Demonstrates dynamic instantiation of polymorphic subclasses.
     */
    public List<Credential> getCredentialsByUser(int userId) {
        List<Credential> list = new ArrayList<>();
        String sql = "SELECT * FROM credentials WHERE user_id = ? ORDER BY created_at DESC";

        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setInt(1, userId);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    String id = rs.getString("id");
                    String title = rs.getString("title");
                    String category = rs.getString("category");
                    String field1 = rs.getString("field1");
                    String field2 = rs.getString("field2");
                    String secretData = rs.getString("secret_data");
                    String extraData = rs.getString("extra_data");
                    LocalDateTime createdAt = LocalDateTime.parse(rs.getString("created_at"));
                    LocalDateTime lastModified = LocalDateTime.parse(rs.getString("last_modified"));

                    Credential cred;
                    if ("Web Login".equalsIgnoreCase(category)) {
                        cred = new WebCredential(id, title, field1, field2, secretData, createdAt, lastModified);
                    } else if ("Credit/Debit Card".equalsIgnoreCase(category)) {
                        cred = new CardCredential(id, title, field1, secretData, field2, extraData, createdAt, lastModified);
                    } else {
                        cred = new SecureNote(id, title, secretData, extraData, createdAt, lastModified);
                    }
                    list.add(cred);
                }
                return list;
            }
        } catch (Exception e) {
            for (StoredItem item : MEMORY_CREDENTIALS) {
                if (item.userId == userId) {
                    list.add(item.credential);
                }
            }
        }
        return list;
    }

    /**
     * Deletes a credential by ID.
     */
    public boolean deleteCredential(String credentialId) {
        String sql = "DELETE FROM credentials WHERE id = ?";
        try (Connection conn = DatabaseManager.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {

            ps.setString(1, credentialId);
            return ps.executeUpdate() > 0;
        } catch (Exception e) {
            return MEMORY_CREDENTIALS.removeIf(item -> item.credential.getId().equals(credentialId));
        }
    }
}
