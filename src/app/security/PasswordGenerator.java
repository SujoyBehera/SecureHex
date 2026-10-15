package app.security;

import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * <h1>Secure Password Generator</h1>
 * <p>Demonstrating Syllabus:
 * <ul>
 *   <li><b>Unit-2:</b> Structural Programming Paradigm (Branching, Iteration, Decision Making, Arrays)</li>
 *   <li><b>Unit-2:</b> Procedural Programming Paradigm (Function Definition, Calling, Arguments)</li>
 * </ul>
 * </p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public final class PasswordGenerator {

    // Character set constants represented as char arrays
    private static final char[] LOWERCASE = "abcdefghijklmnopqrstuvwxyz".toCharArray();
    private static final char[] UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".toCharArray();
    private static final char[] DIGITS = "0123456789".toCharArray();
    private static final char[] SPECIAL = "!@#$%^&*()-_=+[]{}|;:,.<>?".toCharArray();

    private static final SecureRandom RANDOM = new SecureRandom();

    private PasswordGenerator() {
    }

    /**
     * Generates a strong password using default settings (Length: 16, all pools enabled).
     */
    public static String generateDefault() {
        return generate(16, true, true, true, true);
    }

    /**
     * Procedural generator function.
     *
     * @param length Desired length (minimum 8)
     * @param useLower Include lowercase characters
     * @param useUpper Include uppercase characters
     * @param useDigits Include numerical digits
     * @param useSpecial Include symbols and punctuation
     * @return Generated high-entropy password string
     */
    public static String generate(int length, boolean useLower, boolean useUpper, boolean useDigits, boolean useSpecial) {
        if (length < 8) {
            length = 8;
        }

        // Decision making and character pool accumulation
        List<Character> allowedChars = new ArrayList<>();
        List<Character> guaranteedChars = new ArrayList<>();

        if (useLower) {
            for (char c : LOWERCASE) allowedChars.add(c);
            guaranteedChars.add(LOWERCASE[RANDOM.nextInt(LOWERCASE.length)]);
        }
        if (useUpper) {
            for (char c : UPPERCASE) allowedChars.add(c);
            guaranteedChars.add(UPPERCASE[RANDOM.nextInt(UPPERCASE.length)]);
        }
        if (useDigits) {
            for (char c : DIGITS) allowedChars.add(c);
            guaranteedChars.add(DIGITS[RANDOM.nextInt(DIGITS.length)]);
        }
        if (useSpecial) {
            for (char c : SPECIAL) allowedChars.add(c);
            guaranteedChars.add(SPECIAL[RANDOM.nextInt(SPECIAL.length)]);
        }

        // Fallback if no pool is selected
        if (allowedChars.isEmpty()) {
            for (char c : LOWERCASE) allowedChars.add(c);
            for (char c : DIGITS) allowedChars.add(c);
            guaranteedChars.add(LOWERCASE[RANDOM.nextInt(LOWERCASE.length)]);
        }

        // Fill remainder with random selections
        List<Character> resultList = new ArrayList<>(guaranteedChars);
        int remaining = length - guaranteedChars.size();
        for (int i = 0; i < remaining; i++) {
            char chosen = allowedChars.get(RANDOM.nextInt(allowedChars.size()));
            resultList.add(chosen);
        }

        // Shuffle to eliminate position predictability
        Collections.shuffle(resultList, RANDOM);

        // Convert List<Character> to char array and String
        StringBuilder sb = new StringBuilder(resultList.size());
        for (char ch : resultList) {
            sb.append(ch);
        }
        return sb.toString();
    }
}
