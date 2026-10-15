package app.gui;

import app.automata.PasswordDFA;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JProgressBar;

/**
 * <h1>Visual Password Strength Indicator (Automata-Driven)</h1>
 * <p>Demonstrating Syllabus:
 * <ul>
 *   <li><b>Unit-3:</b> Java Swing: MVC & Custom Widgets</li>
 *   <li><b>Unit-5:</b> Finite Automata (DFA) Integration</li>
 * </ul>
 * </p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class PasswordStrengthBar extends JPanel {

    private final JProgressBar progressBar;
    private final JLabel statusLabel;

    public PasswordStrengthBar() {
        setLayout(new BorderLayout(5, 5));
        setOpaque(false);

        progressBar = new JProgressBar(0, 100);
        progressBar.setValue(0);
        progressBar.setStringPainted(false);
        progressBar.setPreferredSize(new Dimension(200, 8));
        progressBar.setBackground(HexDarkTheme.BG_INPUT);
        progressBar.setForeground(HexDarkTheme.ACCENT_RED);
        progressBar.setBorder(null);

        statusLabel = new JLabel("Enter a password");
        statusLabel.setFont(HexDarkTheme.FONT_REGULAR);
        statusLabel.setForeground(HexDarkTheme.TEXT_MUTED);

        add(progressBar, BorderLayout.CENTER);
        add(statusLabel, BorderLayout.SOUTH);
    }

    /**
     * Evaluates the password against the formal DFA and updates visual indicators.
     */
    public void updatePassword(String password) {
        if (password == null || password.isEmpty()) {
            progressBar.setValue(0);
            statusLabel.setText("Password strength: None");
            statusLabel.setForeground(HexDarkTheme.TEXT_MUTED);
            setToolTipText("Enter a password to evaluate using Deterministic Finite Automaton");
            return;
        }

        PasswordDFA.DFAResult result = PasswordDFA.evaluate(password);
        int score = result.getScore();
        progressBar.setValue(score);

        Color barColor;
        String labelText;

        switch (result.getFinalState()) {
            case Q_START:
            case Q_SHORT:
                barColor = HexDarkTheme.ACCENT_RED;
                labelText = "DFA State: Q_SHORT (Too Short < 8 chars)";
                break;
            case Q_WEAK:
                barColor = HexDarkTheme.ACCENT_RED;
                labelText = "DFA State: Q_WEAK (Low Complexity)";
                break;
            case Q_MODERATE:
                barColor = HexDarkTheme.ACCENT_YELLOW;
                labelText = "DFA State: Q_MODERATE (Acceptable)";
                break;
            case Q_STRONG:
                barColor = HexDarkTheme.ACCENT_GREEN;
                labelText = "DFA State: Q_STRONG (High Entropy)";
                break;
            case Q_EXCELLENT:
            default:
                barColor = new Color(0, 230, 118);
                labelText = "DFA State: Q_EXCELLENT (Enterprise Grade)";
                break;
        }

        progressBar.setForeground(barColor);
        statusLabel.setText(labelText);
        statusLabel.setForeground(barColor);

        // Tooltip feedback
        if (!result.getFeedback().isEmpty()) {
            setToolTipText("<html>Suggestions:<br>• " + String.join("<br>• ", result.getFeedback()) + "</html>");
        } else {
            setToolTipText("Password satisfies all formal DFA criteria");
        }
    }
}
