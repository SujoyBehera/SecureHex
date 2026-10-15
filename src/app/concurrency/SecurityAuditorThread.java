package app.concurrency;

import app.automata.PasswordDFA;
import app.model.Credential;
import app.model.WebCredential;
import app.security.EncryptionService;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Consumer;
import javax.swing.SwingUtilities;

/**
 * <h1>Asynchronous Security Auditor Thread</h1>
 * <p>Demonstrating Syllabus <b>Unit-3: Concurrent Programming Paradigm - Thread classes and methods</b>.</p>
 * <p>
 * Performs background inspection of the user's vault to identify weak passwords (using {@link PasswordDFA}),
 * reused/duplicate passwords across different accounts, and security hygiene issues.
 * </p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class SecurityAuditorThread extends Thread {

    public static class AuditReport {
        private final int totalInspected;
        private final int weakCount;
        private final int reusedCount;
        private final List<String> issues;

        public AuditReport(int totalInspected, int weakCount, int reusedCount, List<String> issues) {
            this.totalInspected = totalInspected;
            this.weakCount = weakCount;
            this.reusedCount = reusedCount;
            this.issues = issues;
        }

        public int getTotalInspected() {
            return totalInspected;
        }

        public int getWeakCount() {
            return weakCount;
        }

        public int getReusedCount() {
            return reusedCount;
        }

        public List<String> getIssues() {
            return issues;
        }

        public boolean isAllClean() {
            return weakCount == 0 && reusedCount == 0;
        }
    }

    private final List<Credential> credentials;
    private final String masterPassword;
    private final Consumer<AuditReport> onComplete;

    public SecurityAuditorThread(List<Credential> credentials, String masterPassword, Consumer<AuditReport> onComplete) {
        super("SecureHex-SecurityAuditor-Worker");
        this.credentials = new ArrayList<>(credentials);
        this.masterPassword = masterPassword;
        this.onComplete = onComplete;
    }

    @Override
    public void run() {
        int weakCount = 0;
        List<String> issues = new ArrayList<>();
        Map<String, List<String>> passwordOccurrences = new HashMap<>();

        // Inspect credentials asynchronously
        for (Credential cred : credentials) {
            if (cred instanceof WebCredential) {
                WebCredential wc = (WebCredential) cred;
                try {
                    String decrypted = EncryptionService.decrypt(wc.getEncryptedPassword(), masterPassword);

                    // Formal DFA Automata evaluation
                    PasswordDFA.DFAResult result = PasswordDFA.evaluate(decrypted);
                    if (!result.isAccepted()) {
                        weakCount++;
                        issues.add("Weak password on '" + cred.getTitle() + "': " +
                                   result.getFinalState().getDescription());
                    }

                    // Track duplicate passwords across services
                    passwordOccurrences.computeIfAbsent(decrypted, k -> new ArrayList<>()).add(cred.getTitle());
                } catch (Exception e) {
                    issues.add("Decryption failed for '" + cred.getTitle() + "'");
                }
            }
        }

        // Count reused passwords
        int reusedCount = 0;
        for (Map.Entry<String, List<String>> entry : passwordOccurrences.entrySet()) {
            if (entry.getValue().size() > 1) {
                reusedCount += entry.getValue().size();
                issues.add("Password reused across accounts: " + String.join(", ", entry.getValue()));
            }
        }

        AuditReport report = new AuditReport(credentials.size(), weakCount, reusedCount, issues);

        // Safely notify UI on the Event Dispatch Thread
        if (onComplete != null) {
            SwingUtilities.invokeLater(() -> onComplete.accept(report));
        }
    }
}
