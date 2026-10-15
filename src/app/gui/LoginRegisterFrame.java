package app.gui;

import app.dao.UserDAO;
import app.model.User;
import app.security.PasswordHasher;
import java.awt.BorderLayout;
import java.awt.CardLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;

/**
 * <h1>Authentication Frame (Sign In & Registration)</h1>
 * <p>Demonstrating Syllabus:
 * <ul>
 *   <li><b>Unit-2:</b> Procedural Validation & Class Encapsulation</li>
 *   <li><b>Unit-3:</b> Java Swing: Model View Controller (MVC) Architecture and Event Listeners</li>
 *   <li><b>Unit-5:</b> Dynamic DFA Password Validation Binding</li>
 * </ul>
 * </p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class LoginRegisterFrame extends JFrame {

    private final UserDAO userDAO;
    private CardLayout cardLayout;
    private JPanel containerPanel;

    // Login fields
    private JTextField loginEmailField;
    private JPasswordField loginPasswordField;
    private int loginAttemptsRemaining = 3;

    // Register fields
    private JTextField regNameField;
    private JTextField regEmailField;
    private JPasswordField regPasswordField;
    private JPasswordField regConfirmField;
    private PasswordStrengthBar strengthBar;

    public LoginRegisterFrame() {
        super("SecureHex - Secure Credential Management System");
        this.userDAO = new UserDAO();
        initUI();
    }

    private void initUI() {
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(460, 580);
        setLocationRelativeTo(null);
        getContentPane().setBackground(HexDarkTheme.BG_DARK);
        setLayout(new BorderLayout());

        cardLayout = new CardLayout();
        containerPanel = new JPanel(cardLayout);
        containerPanel.setOpaque(false);

        containerPanel.add(createLoginCard(), "LOGIN");
        containerPanel.add(createRegisterCard(), "REGISTER");

        add(containerPanel, BorderLayout.CENTER);
    }

    private JPanel createLoginCard() {
        JPanel card = HexDarkTheme.createCard();
        card.setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(8, 8, 8, 8);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        // Title
        JLabel titleLbl = new JLabel("🛡️ SecureHex", SwingConstants.CENTER);
        titleLbl.setFont(HexDarkTheme.FONT_TITLE);
        titleLbl.setForeground(HexDarkTheme.ACCENT_GREEN);
        gbc.gridx = 0; gbc.gridy = 0; gbc.gridwidth = 2;
        card.add(titleLbl, gbc);

        JLabel subtitleLbl = new JLabel("Secure Credential Management System", SwingConstants.CENTER);
        subtitleLbl.setFont(HexDarkTheme.FONT_REGULAR);
        subtitleLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        gbc.gridy = 1;
        card.add(subtitleLbl, gbc);

        // Email
        gbc.gridwidth = 1;
        gbc.gridy = 2; gbc.gridx = 0;
        JLabel emailLbl = new JLabel("Registered Email:");
        emailLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        card.add(emailLbl, gbc);

        gbc.gridx = 1;
        loginEmailField = HexDarkTheme.createTextField(18);
        card.add(loginEmailField, gbc);

        // Password
        gbc.gridy = 3; gbc.gridx = 0;
        JLabel pwdLbl = new JLabel("Master Password:");
        pwdLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        card.add(pwdLbl, gbc);

        gbc.gridx = 1;
        loginPasswordField = HexDarkTheme.createPasswordField(18);
        card.add(loginPasswordField, gbc);

        // Login Button
        gbc.gridy = 4; gbc.gridx = 0; gbc.gridwidth = 2;
        JButton loginBtn = HexDarkTheme.createButton("Unlock Vault", HexDarkTheme.ACCENT_GREEN, HexDarkTheme.TEXT_PRIMARY);
        loginBtn.addActionListener(e -> performLogin());
        card.add(loginBtn, gbc);

        // Switch to Register
        gbc.gridy = 5;
        JButton switchBtn = HexDarkTheme.createButton("Don't have a vault? Register New Account", HexDarkTheme.BG_CARD, HexDarkTheme.ACCENT_BLUE);
        switchBtn.addActionListener(e -> cardLayout.show(containerPanel, "REGISTER"));
        card.add(switchBtn, gbc);

        return card;
    }

    private JPanel createRegisterCard() {
        JPanel card = HexDarkTheme.createCard();
        card.setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(6, 6, 6, 6);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        JLabel titleLbl = new JLabel("Create Master Vault", SwingConstants.CENTER);
        titleLbl.setFont(HexDarkTheme.FONT_TITLE);
        titleLbl.setForeground(HexDarkTheme.ACCENT_BLUE);
        gbc.gridx = 0; gbc.gridy = 0; gbc.gridwidth = 2;
        card.add(titleLbl, gbc);

        // Name
        gbc.gridwidth = 1;
        gbc.gridy = 1; gbc.gridx = 0;
        JLabel nameLbl = new JLabel("Full Name:");
        nameLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        card.add(nameLbl, gbc);

        gbc.gridx = 1;
        regNameField = HexDarkTheme.createTextField(18);
        card.add(regNameField, gbc);

        // Email
        gbc.gridy = 2; gbc.gridx = 0;
        JLabel emailLbl = new JLabel("Email Address:");
        emailLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        card.add(emailLbl, gbc);

        gbc.gridx = 1;
        regEmailField = HexDarkTheme.createTextField(18);
        card.add(regEmailField, gbc);

        // Master Password
        gbc.gridy = 3; gbc.gridx = 0;
        JLabel pwdLbl = new JLabel("Master Password:");
        pwdLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        card.add(pwdLbl, gbc);

        gbc.gridx = 1;
        regPasswordField = HexDarkTheme.createPasswordField(18);
        card.add(regPasswordField, gbc);

        // Confirm Password
        gbc.gridy = 4; gbc.gridx = 0;
        JLabel confLbl = new JLabel("Confirm Password:");
        confLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        card.add(confLbl, gbc);

        gbc.gridx = 1;
        regConfirmField = HexDarkTheme.createPasswordField(18);
        card.add(regConfirmField, gbc);

        // DFA Password Strength Bar
        gbc.gridy = 5; gbc.gridx = 0; gbc.gridwidth = 2;
        strengthBar = new PasswordStrengthBar();
        card.add(strengthBar, gbc);

        // Real-time DFA evaluation listener
        regPasswordField.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent e) { update(); }
            @Override
            public void removeUpdate(DocumentEvent e) { update(); }
            @Override
            public void changedUpdate(DocumentEvent e) { update(); }
            private void update() {
                strengthBar.updatePassword(new String(regPasswordField.getPassword()));
            }
        });

        // Register Button
        gbc.gridy = 6;
        JButton regBtn = HexDarkTheme.createButton("Create Encrypted Vault", HexDarkTheme.ACCENT_BLUE, HexDarkTheme.TEXT_PRIMARY);
        regBtn.addActionListener(e -> performRegister());
        card.add(regBtn, gbc);

        // Back to Login
        gbc.gridy = 7;
        JButton backBtn = HexDarkTheme.createButton("Already registered? Sign In", HexDarkTheme.BG_CARD, HexDarkTheme.TEXT_MUTED);
        backBtn.addActionListener(e -> cardLayout.show(containerPanel, "LOGIN"));
        card.add(backBtn, gbc);

        return card;
    }

    private void performLogin() {
        if (loginAttemptsRemaining <= 0) {
            JOptionPane.showMessageDialog(this, "Maximum login attempts exceeded. Vault is locked for security.", "Security Lockout", JOptionPane.ERROR_MESSAGE);
            return;
        }

        String email = loginEmailField.getText().trim().toLowerCase();
        String pwd = new String(loginPasswordField.getPassword());

        if (email.isEmpty() || pwd.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Please enter both Email and Master Password", "Validation Error", JOptionPane.WARNING_MESSAGE);
            return;
        }

        User user = userDAO.findByEmail(email);
        if (user != null && PasswordHasher.verifyPassword(pwd, user.getPasswordHash(), user.getSalt())) {
            userDAO.updateLastLogin(user.getId());
            loginAttemptsRemaining = 3;

            // Open Dashboard
            dispose();
            DashboardFrame dashboard = new DashboardFrame(user, pwd);
            dashboard.setVisible(true);
        } else {
            loginAttemptsRemaining--;
            if (loginAttemptsRemaining > 0) {
                JOptionPane.showMessageDialog(this,
                        "Invalid credentials. Attempts remaining: " + loginAttemptsRemaining,
                        "Login Failed", JOptionPane.ERROR_MESSAGE);
            } else {
                JOptionPane.showMessageDialog(this,
                        "Maximum login attempts reached. Account locked for protection.",
                        "Account Locked", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void performRegister() {
        String name = regNameField.getText().trim();
        String email = regEmailField.getText().trim().toLowerCase();
        String pwd = new String(regPasswordField.getPassword());
        String conf = new String(regConfirmField.getPassword());

        if (name.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Name cannot be empty", "Error", JOptionPane.WARNING_MESSAGE);
            return;
        }
        if (email.isEmpty() || !email.contains("@")) {
            JOptionPane.showMessageDialog(this, "Please enter a valid email address", "Error", JOptionPane.WARNING_MESSAGE);
            return;
        }
        if (pwd.length() < 8) {
            JOptionPane.showMessageDialog(this, "Master Password must be at least 8 characters long", "Error", JOptionPane.WARNING_MESSAGE);
            return;
        }
        if (!pwd.equals(conf)) {
            JOptionPane.showMessageDialog(this, "Passwords do not match", "Error", JOptionPane.WARNING_MESSAGE);
            return;
        }

        String salt = PasswordHasher.generateSalt();
        String hash = PasswordHasher.hashPassword(pwd, salt);
        User newUser = new User(name, email, hash, salt);

        boolean success = userDAO.registerUser(newUser);
        if (success) {
            JOptionPane.showMessageDialog(this, "Account created successfully! Please sign in with your master credentials.", "Success", JOptionPane.INFORMATION_MESSAGE);
            loginEmailField.setText(email);
            cardLayout.show(containerPanel, "LOGIN");
        } else {
            JOptionPane.showMessageDialog(this, "An account with this email already exists.", "Registration Failed", JOptionPane.ERROR_MESSAGE);
        }
    }
}
