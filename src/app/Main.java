package app;

import app.dao.DatabaseManager;
import app.gui.LoginRegisterFrame;
import java.awt.GraphicsEnvironment;
import java.util.Scanner;
import javax.swing.SwingUtilities;
import javax.swing.UIManager;

/**
 * <h1>SecureHex - Application Entry Point</h1>
 * <p>
 * Advanced Programming Practice (APP - 21CSC203P) Course Project.<br>
 * Demonstrating Multi-Paradigm Integration:
 * <ul>
 *   <li><b>Unit-1:</b> Structured Program Theorem, Memory Allocation & Object Serialization</li>
 *   <li><b>Unit-2:</b> Object-Oriented Paradigm (Abstraction, Encapsulation, Inheritance, Polymorphism, Tagging Interfaces)</li>
 *   <li><b>Unit-3:</b> Concurrent Programming (Multithreading Daemon) & Declarative JDBC / MySQL Integration</li>
 *   <li><b>Unit-3:</b> Graphical User Interface Paradigm (Java Swing MVC)</li>
 *   <li><b>Unit-5:</b> Finite Automata Paradigm (Deterministic Finite Automaton for Password Validation)</li>
 * </ul>
 * </p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class Main {

    public static final String APP_NAME = "SecureHex";
    public static final String VERSION = "2.0 (APP Edition)";

    public static void main(String[] args) {
        // Print Console Banner
        printBanner();

        // Check if explicitly requested CLI mode or running in headless environment
        boolean isHeadless = GraphicsEnvironment.isHeadless();
        boolean forceCli = args.length > 0 && "--cli".equalsIgnoreCase(args[0]);

        // Initialize Database Layer (Declarative JDBC / MySQL)
        DatabaseManager.initialize();

        if (isHeadless || forceCli) {
            System.out.println("[SecureHex] Starting in CLI Demonstration Mode...");
            runCliMode();
        } else {
            System.out.println("[SecureHex] Starting Java Swing Graphical User Interface (MVC)...");
            launchGui();
        }
    }

    private static void printBanner() {
        System.out.println("==========================================================");
        System.out.println("                  🛡️ " + APP_NAME + " " + VERSION);
        System.out.println("       Enterprise Secure Credential Management System");
        System.out.println("   Course: 21CSC203P - Advanced Programming Practice (APP)");
        System.out.println("==========================================================");
    }

    /**
     * Launches the Swing GUI on the Event Dispatch Thread (EDT).
     */
    private static void launchGui() {
        SwingUtilities.invokeLater(() -> {
            try {
                // Apply system look and feel if available
                UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName());
            } catch (Exception ignored) {
            }

            LoginRegisterFrame frame = new LoginRegisterFrame();
            frame.setVisible(true);
        });
    }

    /**
     * Fallback interactive console mode demonstrating procedural and structural constructs.
     */
    private static void runCliMode() {
        Scanner scanner = new Scanner(System.in);
        System.out.println("\nSelect Option:");
        System.out.println("1. Launch Swing GUI Desktop App");
        System.out.println("2. View Syllabus Paradigm Mapping");
        System.out.println("3. Exit");
        System.out.print("Choice: ");

        if (scanner.hasNextInt()) {
            int choice = scanner.nextInt();
            scanner.nextLine();
            if (choice == 1) {
                launchGui();
            } else if (choice == 2) {
                printParadigmSummary();
            } else {
                System.out.println("Goodbye from SecureHex!");
            }
        }
    }

    private static void printParadigmSummary() {
        System.out.println("\n--- Syllabus Paradigm Implementation Summary ---");
        System.out.println("• Unit 1: Object Serialization in Credential model & Memory wiping");
        System.out.println("• Unit 2: Credential class hierarchy (WebCredential, CardCredential, SecureNote), Tagging Interface (Auditable)");
        System.out.println("• Unit 3: AutoLockManager Daemon Thread, SecurityAuditorThread, MySQL JDBC DAO, Swing MVC GUI");
        System.out.println("• Unit 5: PasswordDFA Deterministic Finite Automaton (Q_START -> Q_EXCELLENT)");
        System.out.println("-------------------------------------------------\n");
    }
}
