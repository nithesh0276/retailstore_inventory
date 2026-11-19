package com.retailstore.exception;

/**
 * Custom checked exception thrown when an attempted sale quantity exceeds available stock.
 * Course: 25ITT32 Java Programming (Unit 3: User-defined Exceptions)
 */
public class InsufficientStockException extends Exception {
    private final int productId;
    private final String productName;
    private final int availableStock;
    private final int requestedQuantity;

    public InsufficientStockException(String message, int productId, String productName, int availableStock, int requestedQuantity) {
        super(String.format("%s [Product #%d '%s']: Available Stock = %d, Requested = %d (Shortfall = %d units)",
                message, productId, productName, availableStock, requestedQuantity, (requestedQuantity - availableStock)));
        this.productId = productId;
        this.productName = productName;
        this.availableStock = availableStock;
        this.requestedQuantity = requestedQuantity;
    }

    public int getProductId() {
        return productId;
    }

    public String getProductName() {
        return productName;
    }

    public int getAvailableStock() {
        return availableStock;
    }

    public int getRequestedQuantity() {
        return requestedQuantity;
    }

    public int getShortfall() {
        return requestedQuantity - availableStock;
    }
}
