package app.gui;

import app.dao.CredentialDAO;
import app.model.CardCredential;
import app.model.Credential;
import app.model.SecureNote;
import app.model.User;
import app.model.WebCredential;
import app.security.EncryptionService;
import app.security.PasswordGenerator;
import java.awt.BorderLayout;
import java.awt.CardLayout;
import java.awt.Frame;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;

/**
 * <h1>Add Credential Modal Dialog</h1>
 * <p>Demonstrating Syllabus:
 * <ul>
 *   <li><b>Unit-2:</b> Polymorphic Object Instantiation</li>
 *   <li><b>Unit-3:</b> Java Swing: Widgets, Layouts, and Event Handlers</li>
 * </ul>
 * </p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class AddCredentialDialog extends JDialog {

    private final User user;
    private final String masterPassword;
    private final CredentialDAO credentialDAO;
    private final Runnable onSavedCallback;

    private JComboBox<String> categoryCombo;
    private JTextField titleField;

    // Web form fields
    private JTextField urlField;
    private JTextField usernameField;
    private JPasswordField passwordField;

    // Card form fields
    private JTextField cardholderField;
    private JTextField cardNumberField;
    private JTextField expiryField;
    private JPasswordField cvvField;

    // Note form fields
    private JTextArea noteArea;
    private JTextField tagsField;

    private CardLayout cardLayout;
    private JPanel dynamicPanel;

    public AddCredentialDialog(Frame owner, User user, String masterPassword, CredentialDAO credentialDAO, Runnable onSavedCallback) {
        super(owner, "SecureHex - Add New Credential", true);
        this.user = user;
        this.masterPassword = masterPassword;
        this.credentialDAO = credentialDAO;
        this.onSavedCallback = onSavedCallback;

        initUI();
    }

    private void initUI() {
        setSize(520, 500);
        setLocationRelativeTo(getOwner());
        setLayout(new BorderLayout());
        getContentPane().setBackground(HexDarkTheme.BG_DARK);

        JPanel mainPanel = HexDarkTheme.createCard();
        mainPanel.setLayout(new BorderLayout(15, 15));

        // Top Header & Category Selector
        JPanel topPanel = new JPanel(new GridBagLayout());
        topPanel.setOpaque(false);
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(6, 6, 6, 6);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        JLabel titleLbl = new JLabel("Add Vault Item");
        titleLbl.setFont(HexDarkTheme.FONT_TITLE);
        titleLbl.setForeground(HexDarkTheme.TEXT_PRIMARY);
        gbc.gridx = 0; gbc.gridy = 0; gbc.gridwidth = 2;
        topPanel.add(titleLbl, gbc);

        gbc.gridwidth = 1;
        gbc.gridy = 1; gbc.gridx = 0;
        JLabel catLbl = new JLabel("Item Type:");
        catLbl.setFont(HexDarkTheme.FONT_BOLD);
        catLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        topPanel.add(catLbl, gbc);

        gbc.gridx = 1;
        categoryCombo = new JComboBox<>(new String[]{"Web Login", "Credit/Debit Card", "Secure Note"});
        categoryCombo.setBackground(HexDarkTheme.BG_INPUT);
        categoryCombo.setForeground(HexDarkTheme.TEXT_PRIMARY);
        topPanel.add(categoryCombo, gbc);

        gbc.gridy = 2; gbc.gridx = 0;
        JLabel nameLbl = new JLabel("Title / Service:");
        nameLbl.setFont(HexDarkTheme.FONT_BOLD);
        nameLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        topPanel.add(nameLbl, gbc);

        gbc.gridx = 1;
        titleField = HexDarkTheme.createTextField(20);
        topPanel.add(titleField, gbc);

        mainPanel.add(topPanel, BorderLayout.NORTH);

        // Dynamic Card Panels for each Category
        cardLayout = new CardLayout();
        dynamicPanel = new JPanel(cardLayout);
        dynamicPanel.setOpaque(false);

        dynamicPanel.add(createWebPanel(), "Web Login");
        dynamicPanel.add(createCardPanel(), "Credit/Debit Card");
        dynamicPanel.add(createNotePanel(), "Secure Note");

        categoryCombo.addActionListener(e -> {
            String selected = (String) categoryCombo.getSelectedItem();
            cardLayout.show(dynamicPanel, selected);
        });

        mainPanel.add(dynamicPanel, BorderLayout.CENTER);

        // Bottom Actions
        JPanel bottomPanel = new JPanel();
        bottomPanel.setOpaque(false);

        JButton saveBtn = HexDarkTheme.createButton("💾 Save Encrypted", HexDarkTheme.ACCENT_GREEN, HexDarkTheme.TEXT_PRIMARY);
        JButton cancelBtn = HexDarkTheme.createButton("Cancel", HexDarkTheme.BG_INPUT, HexDarkTheme.TEXT_MUTED);

        saveBtn.addActionListener(e -> saveCredential());
        cancelBtn.addActionListener(e -> dispose());

        bottomPanel.add(saveBtn);
        bottomPanel.add(cancelBtn);

        mainPanel.add(bottomPanel, BorderLayout.SOUTH);

        add(mainPanel, BorderLayout.CENTER);
    }

    private JPanel createWebPanel() {
        JPanel p = new JPanel(new GridBagLayout());
        p.setOpaque(false);
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(6, 6, 6, 6);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        gbc.gridx = 0; gbc.gridy = 0;
        JLabel urlLbl = new JLabel("Website URL:");
        urlLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        p.add(urlLbl, gbc);

        gbc.gridx = 1;
        urlField = HexDarkTheme.createTextField(18);
        p.add(urlField, gbc);

        gbc.gridx = 0; gbc.gridy = 1;
        JLabel userLbl = new JLabel("Username / Email:");
        userLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        p.add(userLbl, gbc);

        gbc.gridx = 1;
        usernameField = HexDarkTheme.createTextField(18);
        p.add(usernameField, gbc);

        gbc.gridx = 0; gbc.gridy = 2;
        JLabel pwdLbl = new JLabel("Password:");
        pwdLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        p.add(pwdLbl, gbc);

        gbc.gridx = 1;
        passwordField = HexDarkTheme.createPasswordField(18);
        p.add(passwordField, gbc);

        gbc.gridx = 1; gbc.gridy = 3;
        JButton genBtn = HexDarkTheme.createButton("⚡ Generate Random Password", HexDarkTheme.BG_INPUT, HexDarkTheme.ACCENT_BLUE);
        genBtn.addActionListener(e -> {
            String gen = PasswordGenerator.generateDefault();
            passwordField.setText(gen);
        });
        p.add(genBtn, gbc);

        return p;
    }

    private JPanel createCardPanel() {
        JPanel p = new JPanel(new GridBagLayout());
        p.setOpaque(false);
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(6, 6, 6, 6);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        gbc.gridx = 0; gbc.gridy = 0;
        JLabel holderLbl = new JLabel("Cardholder Name:");
        holderLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        p.add(holderLbl, gbc);

        gbc.gridx = 1;
        cardholderField = HexDarkTheme.createTextField(18);
        p.add(cardholderField, gbc);

        gbc.gridx = 0; gbc.gridy = 1;
        JLabel numLbl = new JLabel("Card Number:");
        numLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        p.add(numLbl, gbc);

        gbc.gridx = 1;
        cardNumberField = HexDarkTheme.createTextField(18);
        p.add(cardNumberField, gbc);

        gbc.gridx = 0; gbc.gridy = 2;
        JLabel expLbl = new JLabel("Expiry (MM/YY):");
        expLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        p.add(expLbl, gbc);

        gbc.gridx = 1;
        expiryField = HexDarkTheme.createTextField(18);
        p.add(expiryField, gbc);

        gbc.gridx = 0; gbc.gridy = 3;
        JLabel cvvLbl = new JLabel("CVV / Security Code:");
        cvvLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        p.add(cvvLbl, gbc);

        gbc.gridx = 1;
        cvvField = HexDarkTheme.createPasswordField(6);
        p.add(cvvField, gbc);

        return p;
    }

    private JPanel createNotePanel() {
        JPanel p = new JPanel(new BorderLayout(8, 8));
        p.setOpaque(false);

        JLabel noteLbl = new JLabel("Secure Note Contents (AES-256 Encrypted):");
        noteLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        p.add(noteLbl, BorderLayout.NORTH);

        noteArea = new JTextArea(6, 25);
        noteArea.setBackground(HexDarkTheme.BG_INPUT);
        noteArea.setForeground(HexDarkTheme.TEXT_PRIMARY);
        noteArea.setFont(HexDarkTheme.FONT_MONO);
        noteArea.setLineWrap(true);
        p.add(new JScrollPane(noteArea), BorderLayout.CENTER);

        JPanel tagPanel = new JPanel(new BorderLayout(5, 5));
        tagPanel.setOpaque(false);
        JLabel tagLbl = new JLabel("Tags (comma separated):");
        tagLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        tagPanel.add(tagLbl, BorderLayout.WEST);
        tagsField = HexDarkTheme.createTextField(15);
        tagPanel.add(tagsField, BorderLayout.CENTER);
        p.add(tagPanel, BorderLayout.SOUTH);

        return p;
    }

    private void saveCredential() {
        String title = titleField.getText().trim();
        if (title.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Title cannot be empty", "Validation Error", JOptionPane.ERROR_MESSAGE);
            return;
        }

        String cat = (String) categoryCombo.getSelectedItem();
        Credential credential;

        try {
            if ("Web Login".equals(cat)) {
                String url = urlField.getText().trim();
                String user = usernameField.getText().trim();
                String pwd = new String(passwordField.getPassword());
                if (pwd.isEmpty()) {
                    JOptionPane.showMessageDialog(this, "Password cannot be empty", "Validation Error", JOptionPane.ERROR_MESSAGE);
                    return;
                }
                String encryptedPassword = EncryptionService.encrypt(pwd, masterPassword);
                credential = new WebCredential(title, url, user, encryptedPassword);

            } else if ("Credit/Debit Card".equals(cat)) {
                String holder = cardholderField.getText().trim();
                String num = cardNumberField.getText().trim();
                String exp = expiryField.getText().trim();
                String cvv = new String(cvvField.getPassword());
                String encryptedNum = EncryptionService.encrypt(num, masterPassword);
                String encryptedCvv = EncryptionService.encrypt(cvv, masterPassword);
                credential = new CardCredential(title, holder, encryptedNum, exp, encryptedCvv);

            } else {
                String note = noteArea.getText();
                String tags = tagsField.getText().trim();
                String encryptedNote = EncryptionService.encrypt(note, masterPassword);
                credential = new SecureNote(title, encryptedNote, tags);
            }

            boolean ok = credentialDAO.saveCredential(user.getId(), credential);
            if (ok) {
                if (onSavedCallback != null) {
                    onSavedCallback.run();
                }
                dispose();
            } else {
                JOptionPane.showMessageDialog(this, "Failed to persist credential to database", "Database Error", JOptionPane.ERROR_MESSAGE);
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Encryption or Save failed: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}
