package app.security;

import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;
import javax.crypto.Cipher;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;

/**
 * <h1>Symmetric Cryptography Engine (AES-256-GCM)</h1>
 * <p>Demonstrating Syllabus:
 * <ul>
 *   <li><b>Unit-1:</b> Dynamic memory allocation for message and object storage</li>
 *   <li><b>Unit-2:</b> Procedural methods, byte arrays, exception handling</li>
 * </ul>
 * </p>
 * <p>Uses AES in Galois/Counter Mode (GCM) providing confidentiality and integrity verification.</p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public final class EncryptionService {

    private static final String ALGORITHM = "AES/GCM/NoPadding";
    private static final int TAG_LENGTH_BIT = 128;
    private static final int IV_LENGTH_BYTE = 12;
    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    private EncryptionService() {
    }

    /**
     * Derives a deterministic 256-bit AES key from the user's master password.
     */
    private static SecretKeySpec deriveKey(String masterPassword) {
        try {
            MessageDigest sha256 = MessageDigest.getInstance("SHA-256");
            byte[] keyBytes = sha256.digest(masterPassword.getBytes(StandardCharsets.UTF_8));
            return new SecretKeySpec(keyBytes, "AES");
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 unavailable", e);
        }
    }

    /**
     * Encrypts plaintext string using AES-256 GCM authenticated encryption.
     *
     * @param plaintext Sensitive string to encrypt
     * @param masterPassword Master password acting as encryption key
     * @return Base64 payload containing (IV + ciphertext + authentication tag)
     */
    public static String encrypt(String plaintext, String masterPassword) {
        if (plaintext == null) {
            return null;
        }
        try {
            byte[] iv = new byte[IV_LENGTH_BYTE];
            SECURE_RANDOM.nextBytes(iv);

            SecretKeySpec secretKey = deriveKey(masterPassword);
            Cipher cipher = Cipher.getInstance(ALGORITHM);
            GCMParameterSpec parameterSpec = new GCMParameterSpec(TAG_LENGTH_BIT, iv);
            cipher.init(Cipher.ENCRYPT_MODE, secretKey, parameterSpec);

            byte[] cipherText = cipher.doFinal(plaintext.getBytes(StandardCharsets.UTF_8));

            // Pack IV + CipherText together
            ByteBuffer byteBuffer = ByteBuffer.allocate(iv.length + cipherText.length);
            byteBuffer.put(iv);
            byteBuffer.put(cipherText);

            return Base64.getEncoder().encodeToString(byteBuffer.array());
        } catch (Exception e) {
            throw new RuntimeException("Encryption failed", e);
        }
    }

    /**
     * Decrypts Base64 payload using AES-256 GCM authenticated encryption.
     *
     * @param encryptedBase64 Encrypted payload containing (IV + ciphertext)
     * @param masterPassword Master password used for decryption
     * @return Decrypted plaintext string
     */
    public static String decrypt(String encryptedBase64, String masterPassword) {
        if (encryptedBase64 == null) {
            return null;
        }
        try {
            byte[] decoded = Base64.getDecoder().decode(encryptedBase64);
            ByteBuffer byteBuffer = ByteBuffer.wrap(decoded);

            byte[] iv = new byte[IV_LENGTH_BYTE];
            byteBuffer.get(iv);

            byte[] cipherText = new byte[byteBuffer.remaining()];
            byteBuffer.get(cipherText);

            SecretKeySpec secretKey = deriveKey(masterPassword);
            Cipher cipher = Cipher.getInstance(ALGORITHM);
            GCMParameterSpec parameterSpec = new GCMParameterSpec(TAG_LENGTH_BIT, iv);
            cipher.init(Cipher.DECRYPT_MODE, secretKey, parameterSpec);

            byte[] plainTextBytes = cipher.doFinal(cipherText);
            return new String(plainTextBytes, StandardCharsets.UTF_8);
        } catch (Exception e) {
            throw new RuntimeException("Decryption failed: Invalid key or corrupted data", e);
        }
    }
}
