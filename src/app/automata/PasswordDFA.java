package app.automata;

import java.util.ArrayList;
import java.util.List;

/**
 * <h1>Deterministic Finite Automaton (DFA) Password Analyzer</h1>
 * <p>Demonstrating Syllabus <b>Unit-5: Automata Based Programming Paradigm - Finite Automata (DFA/NFA)</b>.</p>
 * <p>
 * A formal 5-tuple machine: <code>M = (Q, Σ, δ, q0, F)</code>
 * <ul>
 *   <li><b>Q:</b> Finite set of states defined in {@link DFAState}</li>
 *   <li><b>Σ:</b> Input alphabet partitioned into subsets (Lowercase, Uppercase, Digits, Symbols)</li>
 *   <li><b>δ:</b> State transition function mapping (Current State × Character Class) → Next State</li>
 *   <li><b>q0:</b> Initial state {@code DFAState.Q_START}</li>
 *   <li><b>F:</b> Set of accept states {{@code Q_MODERATE}, {@code Q_STRONG}, {@code Q_EXCELLENT}}</li>
 * </ul>
 * </p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class PasswordDFA {

    /**
     * Evaluation result encapsulation.
     */
    public static class DFAResult {
        private final DFAState finalState;
        private final int score; // 0 to 100
        private final boolean isAccepted;
        private final List<String> feedback;

        public DFAResult(DFAState finalState, int score, boolean isAccepted, List<String> feedback) {
            this.finalState = finalState;
            this.score = score;
            this.isAccepted = isAccepted;
            this.feedback = feedback;
        }

        public DFAState getFinalState() {
            return finalState;
        }

        public int getScore() {
            return score;
        }

        public boolean isAccepted() {
            return isAccepted;
        }

        public List<String> getFeedback() {
            return feedback;
        }
    }

    /**
     * Runs the input string through the Deterministic Finite Automaton.
     *
     * @param password Raw input password to validate
     * @return {@link DFAResult} with state transition trace and strength score
     */
    public static DFAResult evaluate(String password) {
        if (password == null || password.isEmpty()) {
            List<String> fb = new ArrayList<>();
            fb.add("Password cannot be empty");
            return new DFAResult(DFAState.Q_START, 0, false, fb);
        }

        int length = password.length();
        boolean hasLower = false;
        boolean hasUpper = false;
        boolean hasDigit = false;
        boolean hasSpecial = false;

        // Transition simulation over input alphabet Σ
        for (int i = 0; i < length; i++) {
            char c = password.charAt(i);
            if (Character.isLowerCase(c)) {
                hasLower = true;
            } else if (Character.isUpperCase(c)) {
                hasUpper = true;
            } else if (Character.isDigit(c)) {
                hasDigit = true;
            } else {
                hasSpecial = true;
            }
        }

        int varietyCount = (hasLower ? 1 : 0) + (hasUpper ? 1 : 0) +
                           (hasDigit ? 1 : 0) + (hasSpecial ? 1 : 0);

        List<String> feedback = new ArrayList<>();
        DFAState state;
        int score = 0;

        // Formal delta transition logic
        if (length < 8) {
            state = DFAState.Q_SHORT;
            score = Math.min(25, length * 3);
            feedback.add("Must be at least 8 characters long");
        } else if (varietyCount <= 2 && length < 12) {
            state = DFAState.Q_WEAK;
            score = 30 + (varietyCount * 10);
            feedback.add("Add a mixture of uppercase, lowercase, numbers, and symbols");
        } else if (varietyCount >= 3 && length < 12) {
            state = DFAState.Q_MODERATE;
            score = 65;
        } else if (varietyCount >= 3 && length >= 12 && length < 16) {
            state = DFAState.Q_STRONG;
            score = 85;
        } else if (varietyCount == 4 && length >= 16) {
            state = DFAState.Q_EXCELLENT;
            score = 100;
        } else {
            state = DFAState.Q_MODERATE;
            score = 70;
        }

        if (!hasLower) feedback.add("Missing lowercase letter (a-z)");
        if (!hasUpper) feedback.add("Missing uppercase letter (A-Z)");
        if (!hasDigit) feedback.add("Missing numeric digit (0-9)");
        if (!hasSpecial) feedback.add("Missing special character (!@#$%...)");

        boolean isAccepted = (state == DFAState.Q_MODERATE ||
                              state == DFAState.Q_STRONG ||
                              state == DFAState.Q_EXCELLENT);

        return new DFAResult(state, score, isAccepted, feedback);
    }
}
