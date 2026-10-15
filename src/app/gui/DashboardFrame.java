package app.gui;

import app.concurrency.AutoLockManager;
import app.concurrency.SecurityAuditorThread;
import app.dao.CredentialDAO;
import app.dao.DatabaseManager;
import app.model.CardCredential;
import app.model.Credential;
import app.model.SecureNote;
import app.model.User;
import app.model.WebCredential;
import app.security.EncryptionService;
import app.security.PasswordGenerator;
import java.awt.AWTEvent;
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.Toolkit;
import java.awt.datatransfer.StringSelection;
import java.awt.event.AWTEventListener;
import java.util.ArrayList;
import java.util.List;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.RowFilter;
import javax.swing.SwingUtilities;
import javax.swing.Timer;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableRowSorter;

/**
 * <h1>SecureHex Main Vault Dashboard</h1>
 * <p>Demonstrating Syllabus:
 * <ul>
 *   <li><b>Unit-2:</b> Polymorphism (dynamic method calls on {@link Credential})</li>
 *   <li><b>Unit-3:</b> Concurrency (Multithreading via {@link AutoLockManager} and {@link SecurityAuditorThread})</li>
 *   <li><b>Unit-3:</b> Declarative Paradigm (JDBC Query Execution via {@link CredentialDAO})</li>
 *   <li><b>Unit-3:</b> Swing GUI: Model-View-Controller (MVC), Tables, Dialogs, Event Handlers</li>
 * </ul>
 * </p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class DashboardFrame extends JFrame {

    private final User user;
    private final String masterPassword;
    private final CredentialDAO credentialDAO;
    private final AutoLockManager autoLockManager;
    private final List<Credential> credentials;

    private DefaultTableModel tableModel;
    private JTable credentialTable;
    private TableRowSorter<DefaultTableModel> rowSorter;
    private JLabel autoLockLabel;
    private Timer uiCountdownTimer;
    private AWTEventListener activityListener;

    public DashboardFrame(User user, String masterPassword) {
        super("SecureHex Vault - Logged in as " + user.getName());
        this.user = user;
        this.masterPassword = masterPassword;
        this.credentialDAO = new CredentialDAO();
        this.credentials = new ArrayList<>();

        // Unit-3 Concurrency: Inactivity daemon thread (locks vault after 180 seconds of inactivity)
        this.autoLockManager = new AutoLockManager(180, this::triggerAutoLock);

        initUI();
        setupActivityMonitor();
        loadCredentials();
        autoLockManager.start();
    }

    private void initUI() {
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(960, 620);
        setLocationRelativeTo(null);
        getContentPane().setBackground(HexDarkTheme.BG_DARK);
        setLayout(new BorderLayout(10, 10));

        // 1. Header Toolbar
        JPanel headerPanel = HexDarkTheme.createCard();
        headerPanel.setLayout(new BorderLayout());

        JLabel logoLbl = new JLabel("🛡️ SecureHex Vault | " + user.getName() + " (" + user.getEmail() + ")");
        logoLbl.setFont(HexDarkTheme.FONT_HEADER);
        logoLbl.setForeground(HexDarkTheme.ACCENT_GREEN);
        headerPanel.add(logoLbl, BorderLayout.WEST);

        JPanel headerRight = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        headerRight.setOpaque(false);

        autoLockLabel = new JLabel("⏳ Auto-Lock: 180s");
        autoLockLabel.setFont(HexDarkTheme.FONT_MONO);
        autoLockLabel.setForeground(HexDarkTheme.TEXT_MUTED);
        headerRight.add(autoLockLabel);

        JButton lockBtn = HexDarkTheme.createButton("🔒 Lock Vault", HexDarkTheme.BG_INPUT, HexDarkTheme.ACCENT_YELLOW);
        lockBtn.addActionListener(e -> lockVault());
        headerRight.add(lockBtn);

        JButton logoutBtn = HexDarkTheme.createButton("🚪 Logout", HexDarkTheme.BG_INPUT, HexDarkTheme.ACCENT_RED);
        logoutBtn.addActionListener(e -> logout());
        headerRight.add(logoutBtn);

        headerPanel.add(headerRight, BorderLayout.EAST);
        add(headerPanel, BorderLayout.NORTH);

        // 2. Central Table Panel
        JPanel centerPanel = new JPanel(new BorderLayout(10, 10));
        centerPanel.setOpaque(false);

        // Search Bar & Filter
        JPanel searchBar = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 5));
        searchBar.setOpaque(false);
        JLabel searchLbl = new JLabel("🔍 Search Vault:");
        searchLbl.setForeground(HexDarkTheme.TEXT_MUTED);
        searchBar.add(searchLbl);

        JTextField searchField = HexDarkTheme.createTextField(25);
        searchField.getDocument().addDocumentListener(new DocumentListener() {
            @Override
            public void insertUpdate(DocumentEvent e) { filter(); }
            @Override
            public void removeUpdate(DocumentEvent e) { filter(); }
            @Override
            public void changedUpdate(DocumentEvent e) { filter(); }
            private void filter() {
                String txt = searchField.getText().trim();
                if (txt.isEmpty()) {
                    rowSorter.setRowFilter(null);
                } else {
                    rowSorter.setRowFilter(RowFilter.regexFilter("(?i)" + txt));
                }
            }
        });
        searchBar.add(searchField);
        centerPanel.add(searchBar, BorderLayout.NORTH);

        // JTable Configuration
        String[] columnNames = {"Type", "Title / Service", "Account / Resource Details", "Masked Secret", "Modified"};
        tableModel = new DefaultTableModel(columnNames, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };

        credentialTable = new JTable(tableModel);
        rowSorter = new TableRowSorter<>(tableModel);
        credentialTable.setRowSorter(rowSorter);
        HexDarkTheme.styleTable(credentialTable);

        JScrollPane scrollPane = new JScrollPane(credentialTable);
        scrollPane.getViewport().setBackground(HexDarkTheme.BG_CARD);
        scrollPane.setBorder(null);
        centerPanel.add(scrollPane, BorderLayout.CENTER);

        add(centerPanel, BorderLayout.CENTER);

        // 3. Bottom Action Bar
        JPanel bottomPanel = HexDarkTheme.createCard();
        bottomPanel.setLayout(new FlowLayout(FlowLayout.LEFT, 10, 8));

        JButton addBtn = HexDarkTheme.createButton("+ Add Item", HexDarkTheme.ACCENT_GREEN, HexDarkTheme.TEXT_PRIMARY);
        addBtn.addActionListener(e -> openAddDialog());
        bottomPanel.add(addBtn);

        JButton copyBtn = HexDarkTheme.createButton("📋 Copy Secret", HexDarkTheme.BG_INPUT, HexDarkTheme.ACCENT_BLUE);
        copyBtn.addActionListener(e -> copySelectedSecret());
        bottomPanel.add(copyBtn);

        JButton revealBtn = HexDarkTheme.createButton("👁️ Reveal Secret", HexDarkTheme.BG_INPUT, HexDarkTheme.TEXT_PRIMARY);
        revealBtn.addActionListener(e -> revealSelectedSecret());
        bottomPanel.add(revealBtn);

        JButton deleteBtn = HexDarkTheme.createButton("🗑️ Delete", HexDarkTheme.BG_INPUT, HexDarkTheme.ACCENT_RED);
        deleteBtn.addActionListener(e -> deleteSelected());
        bottomPanel.add(deleteBtn);

        JButton genBtn = HexDarkTheme.createButton("⚡ Generate Password", HexDarkTheme.BG_INPUT, HexDarkTheme.ACCENT_YELLOW);
        genBtn.addActionListener(e -> showPasswordGenerator());
        bottomPanel.add(genBtn);

        JButton auditBtn = HexDarkTheme.createButton("🛡️ Run Security Audit (Multithreaded)", HexDarkTheme.ACCENT_BLUE, HexDarkTheme.TEXT_PRIMARY);
        auditBtn.addActionListener(e -> runSecurityAudit());
        bottomPanel.add(auditBtn);

        add(bottomPanel, BorderLayout.SOUTH);

        // 4. UI Timer to display remaining auto-lock seconds
        uiCountdownTimer = new Timer(1000, e -> {
            int remaining = autoLockManager.getRemainingSeconds();
            autoLockLabel.setText("⏳ Auto-Lock: " + remaining + "s");
            if (remaining <= 30) {
                autoLockLabel.setForeground(HexDarkTheme.ACCENT_RED);
            } else {
                autoLockLabel.setForeground(HexDarkTheme.TEXT_MUTED);
            }
        });
        uiCountdownTimer.start();
    }

    private void setupActivityMonitor() {
        // Global listener across the application window to reset inactivity timer
        activityListener = event -> autoLockManager.recordUserActivity();
        Toolkit.getDefaultToolkit().addAWTEventListener(
                activityListener,
                AWTEvent.MOUSE_EVENT_MASK | AWTEvent.KEY_EVENT_MASK | AWTEvent.MOUSE_MOTION_EVENT_MASK
        );
    }

    private void loadCredentials() {
        credentials.clear();
        credentials.addAll(credentialDAO.getCredentialsByUser(user.getId()));

        tableModel.setRowCount(0);
        for (Credential c : credentials) {
            tableModel.addRow(new Object[]{
                    c.getCategory(),
                    c.getTitle(),
                    c.getSummary(),
                    "••••••••••••",
                    c.getLastModifiedAt().toString().replace("T", " ").substring(0, 19)
            });
        }
    }

    private void openAddDialog() {
        AddCredentialDialog dialog = new AddCredentialDialog(this, user, masterPassword, credentialDAO, this::loadCredentials);
        dialog.setVisible(true);
    }

    private Credential getSelectedCredential() {
        int viewRow = credentialTable.getSelectedRow();
        if (viewRow < 0) {
            JOptionPane.showMessageDialog(this, "Please select an item from the table first.", "Notice", JOptionPane.INFORMATION_MESSAGE);
            return null;
        }
        int modelRow = credentialTable.convertRowIndexToModel(viewRow);
        return credentials.get(modelRow);
    }

    private void copySelectedSecret() {
        Credential cred = getSelectedCredential();
        if (cred == null) return;

        try {
            String rawSecret = EncryptionService.decrypt(cred.getPrimarySecret(), masterPassword);
            Toolkit.getDefaultToolkit().getSystemClipboard().setContents(new StringSelection(rawSecret), null);
            JOptionPane.showMessageDialog(this, "Secret copied to clipboard! (Will remain in clipboard)", "Clipboard", JOptionPane.INFORMATION_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Decryption error: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void revealSelectedSecret() {
        Credential cred = getSelectedCredential();
        if (cred == null) return;

        try {
            String rawSecret = EncryptionService.decrypt(cred.getPrimarySecret(), masterPassword);
            String message;
            if (cred instanceof WebCredential) {
                WebCredential wc = (WebCredential) cred;
                message = "Service: " + wc.getTitle() + "\nURL: " + wc.getUrl() +
                          "\nUsername: " + wc.getUsername() + "\nPassword: " + rawSecret;
            } else if (cred instanceof CardCredential) {
                CardCredential cc = (CardCredential) cred;
                String cvv = EncryptionService.decrypt(cc.getCvvEncrypted(), masterPassword);
                message = "Card: " + cc.getTitle() + "\nHolder: " + cc.getCardholderName() +
                          "\nCard Number: " + rawSecret + "\nExpiry: " + cc.getExpiryDate() + "\nCVV: " + cvv;
            } else {
                SecureNote sn = (SecureNote) cred;
                message = "Note: " + sn.getTitle() + "\nTags: " + sn.getTags() + "\n\nContent:\n" + rawSecret;
            }

            JOptionPane.showMessageDialog(this, message, "Decrypted Item Details", JOptionPane.INFORMATION_MESSAGE);
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Decryption error: " + ex.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void deleteSelected() {
        Credential cred = getSelectedCredential();
        if (cred == null) return;

        int confirm = JOptionPane.showConfirmDialog(
                this,
                "Are you sure you want to delete '" + cred.getTitle() + "'?",
                "Confirm Deletion",
                JOptionPane.YES_NO_OPTION
        );
        if (confirm == JOptionPane.YES_OPTION) {
            credentialDAO.deleteCredential(cred.getId());
            loadCredentials();
        }
    }

    private void showPasswordGenerator() {
        String generated = PasswordGenerator.generateDefault();
        int choice = JOptionPane.showOptionDialog(
                this,
                "Generated High-Entropy Password:\n" + generated,
                "Secure Password Generator",
                JOptionPane.DEFAULT_OPTION,
                JOptionPane.INFORMATION_MESSAGE,
                null,
                new String[]{"Copy to Clipboard", "Close"},
                "Copy to Clipboard"
        );
        if (choice == 0) {
            Toolkit.getDefaultToolkit().getSystemClipboard().setContents(new StringSelection(generated), null);
            JOptionPane.showMessageDialog(this, "Copied to clipboard!", "Success", JOptionPane.INFORMATION_MESSAGE);
        }
    }

    private void runSecurityAudit() {
        // Unit-3 Concurrency: Launch background inspection thread
        JOptionPane.showMessageDialog(this, "Starting asynchronous background audit...", "Security Audit", JOptionPane.INFORMATION_MESSAGE);

        SecurityAuditorThread auditor = new SecurityAuditorThread(credentials, masterPassword, report -> {
            StringBuilder sb = new StringBuilder();
            sb.append("=== Asynchronous Security Audit Report ===\n\n");
            sb.append("Total Items Inspected: ").append(report.getTotalInspected()).append("\n");
            sb.append("Weak Passwords (DFA Flagged): ").append(report.getWeakCount()).append("\n");
            sb.append("Reused Passwords Detected: ").append(report.getReusedCount()).append("\n\n");

            if (report.isAllClean()) {
                sb.append("✅ Excellent hygiene! All vault items satisfy security requirements.");
            } else {
                sb.append("⚠️ Warnings & Recommendations:\n");
                for (String issue : report.getIssues()) {
                    sb.append(" • ").append(issue).append("\n");
                }
            }

            JOptionPane.showMessageDialog(this, sb.toString(), "Vault Security Report",
                    report.isAllClean() ? JOptionPane.INFORMATION_MESSAGE : JOptionPane.WARNING_MESSAGE);
        });
        auditor.start();
    }

    private void cleanup() {
        if (uiCountdownTimer != null) uiCountdownTimer.stop();
        if (autoLockManager != null) autoLockManager.stop();
        if (activityListener != null) {
            Toolkit.getDefaultToolkit().removeAWTEventListener(activityListener);
        }
    }

    private void lockVault() {
        cleanup();
        dispose();
        LoginRegisterFrame loginFrame = new LoginRegisterFrame();
        loginFrame.setVisible(true);
    }

    private void triggerAutoLock() {
        cleanup();
        dispose();
        LoginRegisterFrame loginFrame = new LoginRegisterFrame();
        loginFrame.setVisible(true);
        JOptionPane.showMessageDialog(loginFrame, "Vault has been locked automatically due to 3 minutes of inactivity.", "Security Auto-Lock", JOptionPane.WARNING_MESSAGE);
    }

    private void logout() {
        int confirm = JOptionPane.showConfirmDialog(this, "Log out from SecureHex?", "Logout", JOptionPane.YES_NO_OPTION);
        if (confirm == JOptionPane.YES_OPTION) {
            cleanup();
            dispose();
            LoginRegisterFrame loginFrame = new LoginRegisterFrame();
            loginFrame.setVisible(true);
        }
    }
}
