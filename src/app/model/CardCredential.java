package app.model;

import java.time.LocalDateTime;

/**
 * <h1>Payment Card Credential Entity</h1>
 * <p>Demonstrating Syllabus <b>Unit-2: Inheritance & Polymorphism</b>.</p>
 *
 * @author SecureHex Development Team (Group of 3)
 */
public class CardCredential extends Credential {
    private static final long serialVersionUID = 1L;

    private String cardholderName;
    private String cardNumberEncrypted;
    private String expiryDate;
    private String cvvEncrypted;

    public CardCredential(String title, String cardholderName, String cardNumberEncrypted,
                          String expiryDate, String cvvEncrypted) {
        super(title, "Credit/Debit Card");
        this.cardholderName = cardholderName;
        this.cardNumberEncrypted = cardNumberEncrypted;
        this.expiryDate = expiryDate;
        this.cvvEncrypted = cvvEncrypted;
    }

    public CardCredential(String id, String title, String cardholderName, String cardNumberEncrypted,
                          String expiryDate, String cvvEncrypted,
                          LocalDateTime createdAt, LocalDateTime lastModifiedAt) {
        super(id, title, "Credit/Debit Card", createdAt, lastModifiedAt);
        this.cardholderName = cardholderName;
        this.cardNumberEncrypted = cardNumberEncrypted;
        this.expiryDate = expiryDate;
        this.cvvEncrypted = cvvEncrypted;
    }

    public String getCardholderName() {
        return cardholderName;
    }

    public void setCardholderName(String cardholderName) {
        this.cardholderName = cardholderName;
        updateLastModified();
    }

    public String getCardNumberEncrypted() {
        return cardNumberEncrypted;
    }

    public void setCardNumberEncrypted(String cardNumberEncrypted) {
        this.cardNumberEncrypted = cardNumberEncrypted;
        updateLastModified();
    }

    public String getExpiryDate() {
        return expiryDate;
    }

    public void setExpiryDate(String expiryDate) {
        this.expiryDate = expiryDate;
        updateLastModified();
    }

    public String getCvvEncrypted() {
        return cvvEncrypted;
    }

    public void setCvvEncrypted(String cvvEncrypted) {
        this.cvvEncrypted = cvvEncrypted;
        updateLastModified();
    }

    @Override
    public String getSummary() {
        return "Cardholder: " + cardholderName + " | Exp: " + expiryDate;
    }

    @Override
    public String getMaskedDetails() {
        return "Holder: " + cardholderName + " | Number: •••• •••• •••• [Card] | Exp: " + expiryDate;
    }

    @Override
    public String getPrimarySecret() {
        return cardNumberEncrypted;
    }
}
