package app.gui;

import java.awt.Color;
import java.awt.Component;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.JTableHeader;

/**
 * <h1>Modern Hex-Dark Theme & UI Toolkit</h1>
 * <p>Demonstrating Syllabus <b>Unit-3: Java Swing: Widgets and Styling</b>.</p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public final class HexDarkTheme {

    // Color Palette
    public static final Color BG_DARK = new Color(13, 17, 23);         // #0D1117 (Main background)
    public static final Color BG_CARD = new Color(22, 27, 34);         // #161B22 (Card panels)
    public static final Color BG_INPUT = new Color(33, 38, 45);        // #21262D (Inputs)
    public static final Color BORDER = new Color(48, 54, 61);          // #30363D
    public static final Color ACCENT_GREEN = new Color(46, 160, 67);   // #2EA043 (Neon green)
    public static final Color ACCENT_BLUE = new Color(88, 166, 255);   // #58A6FF
    public static final Color ACCENT_RED = new Color(248, 81, 73);     // #F85149
    public static final Color ACCENT_YELLOW = new Color(210, 153, 34); // #D29922
    public static final Color TEXT_PRIMARY = new Color(240, 246, 252); // High contrast text
    public static final Color TEXT_MUTED = new Color(139, 148, 158);   // Secondary text

    // Typography
    public static final Font FONT_TITLE = new Font("Segoe UI", Font.BOLD, 22);
    public static final Font FONT_HEADER = new Font("Segoe UI", Font.BOLD, 15);
    public static final Font FONT_REGULAR = new Font("Segoe UI", Font.PLAIN, 13);
    public static final Font FONT_BOLD = new Font("Segoe UI", Font.BOLD, 13);
    public static final Font FONT_MONO = new Font("Consolas", Font.PLAIN, 13);

    private HexDarkTheme() {
    }

    public static JButton createButton(String text, Color bg, Color fg) {
        JButton btn = new JButton(text) {
            @Override
            protected void paintComponent(Graphics g) {
                Graphics2D g2 = (Graphics2D) g.create();
                g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
                g2.setColor(getBackground());
                g2.fillRoundRect(0, 0, getWidth(), getHeight(), 8, 8);
                super.paintComponent(g);
                g2.dispose();
            }
        };
        btn.setFont(FONT_BOLD);
        btn.setBackground(bg);
        btn.setForeground(fg);
        btn.setFocusPainted(false);
        btn.setContentAreaFilled(false);
        btn.setBorder(BorderFactory.createEmptyBorder(8, 16, 8, 16));
        btn.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        return btn;
    }

    public static JTextField createTextField(int columns) {
        JTextField tf = new JTextField(columns);
        styleInput(tf);
        return tf;
    }

    public static JPasswordField createPasswordField(int columns) {
        JPasswordField pf = new JPasswordField(columns);
        styleInput(pf);
        return pf;
    }

    private static void styleInput(JTextField tf) {
        tf.setBackground(BG_INPUT);
        tf.setForeground(TEXT_PRIMARY);
        tf.setCaretColor(TEXT_PRIMARY);
        tf.setFont(FONT_REGULAR);
        tf.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(BORDER, 1),
                BorderFactory.createEmptyBorder(6, 10, 6, 10)
        ));
    }

    public static void styleTable(JTable table) {
        table.setBackground(BG_CARD);
        table.setForeground(TEXT_PRIMARY);
        table.setGridColor(BORDER);
        table.setFont(FONT_REGULAR);
        table.setRowHeight(36);
        table.setSelectionBackground(new Color(56, 139, 253, 50));
        table.setSelectionForeground(TEXT_PRIMARY);

        JTableHeader header = table.getTableHeader();
        header.setBackground(BG_DARK);
        header.setForeground(TEXT_MUTED);
        header.setFont(FONT_BOLD);
        header.setPreferredSize(new Dimension(0, 36));
        header.setBorder(BorderFactory.createLineBorder(BORDER));

        table.setDefaultRenderer(Object.class, new DefaultTableCellRenderer() {
            @Override
            public Component getTableCellRendererComponent(JTable t, Object val, boolean isSel, boolean hasFocus, int row, int col) {
                Component c = super.getTableCellRendererComponent(t, val, isSel, false, row, col);
                setBorder(BorderFactory.createEmptyBorder(0, 8, 0, 8));
                if (!isSel) {
                    c.setBackground(row % 2 == 0 ? BG_CARD : BG_DARK);
                }
                return c;
            }
        });
    }

    public static JPanel createCard() {
        JPanel card = new JPanel();
        card.setBackground(BG_CARD);
        card.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createLineBorder(BORDER, 1),
                BorderFactory.createEmptyBorder(16, 16, 16, 16)
        ));
        return card;
    }
}
