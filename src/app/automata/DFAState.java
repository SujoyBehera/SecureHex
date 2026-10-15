package app.automata;

/**
 * <h1>DFA State Representation</h1>
 * <p>Demonstrating Syllabus <b>Unit-5: Automata Based Programming Paradigm - Finite Automata (DFA)</b>.</p>
 * <p>Represents individual states in the password validation state machine: $Q = \{q_0, q_1, \dots, q_k\}$.</p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public enum DFAState {
    Q_START("Initial State / Empty Input"),
    Q_SHORT("Short Length (<8 characters)"),
    Q_WEAK("Basic Length Met, Insufficient Entropy"),
    Q_MODERATE("Moderate Complexity (Length + 2-3 Character Classes)"),
    Q_STRONG("High Complexity (Length >=12 + All 4 Classes)"),
    Q_EXCELLENT("Enterprise Grade (Length >=16 + High Entropy)");

    private final String description;

    DFAState(String description) {
        this.description = description;
    }

    public String getDescription() {
        return description;
    }
}
