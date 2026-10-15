package app.security;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;

/**
 * <h1>Cryptographic Password Hashing Service</h1>
 * <p>Demonstrating Syllabus <b>Unit-2: Procedural & Functional Methods, Modifiers and Operators</b>.</p>
 * <p>Uses SHA-256 with cryptographically secure random salt and constant-time equality check.</p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public final class PasswordHasher {

    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    private PasswordHasher() {
        // Private constructor to enforce static utility access
    }

    /**
     * Generates a cryptographically strong 16-byte random salt.
     *
     * @return Base64 encoded salt string
     */
    public static String generateSalt() {
        byte[] salt = new byte[16];
        SECURE_RANDOM.nextBytes(salt);
        return Base64.getEncoder().encodeToString(salt);
    }

    /**
     * Hashes a plain password with a given salt using SHA-256.
     *
     * @param password Raw plaintext password
     * @param saltBase64 Base64 encoded salt
     * @return Hex-encoded hash string
     */
    public static String hashPassword(String password, String saltBase64) {
        if (password == null || saltBase64 == null) {
            throw new IllegalArgumentException("Password and salt cannot be null");
        }
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] saltBytes = Base64.getDecoder().decode(saltBase64);
            digest.update(saltBytes);
            byte[] hashedBytes = digest.digest(password.getBytes(StandardCharsets.UTF_8));
            return bytesToHex(hashedBytes);
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException("SHA-256 algorithm not available", e);
        }
    }

    /**
     * Verifies a password against an existing hash using constant-time comparison to prevent timing attacks.
     *
     * @param plainPassword Raw password to test
     * @param storedHash Expected hash value
     * @param saltBase64 Salt used during hashing
     * @return true if password matches, false otherwise
     */
    public static boolean verifyPassword(String plainPassword, String storedHash, String saltBase64) {
        String computedHash = hashPassword(plainPassword, saltBase64);
        return MessageDigest.isEqual(
                computedHash.getBytes(StandardCharsets.UTF_8),
                storedHash.getBytes(StandardCharsets.UTF_8)
        );
    }

    private static String bytesToHex(byte[] bytes) {
        StringBuilder sb = new StringBuilder(bytes.length * 2);
        for (byte b : bytes) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }
}
