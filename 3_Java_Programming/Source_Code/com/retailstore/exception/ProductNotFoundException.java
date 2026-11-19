package com.retailstore.exception;

/**
 * Custom checked exception thrown when a requested product SKU cannot be found in the catalog.
 * Course: 25ITT32 Java Programming (Unit 3: User-defined Exceptions)
 */
public class ProductNotFoundException extends Exception {
    private final int productId;

    public ProductNotFoundException(int productId) {
        super(String.format("Product with ID %d does not exist in the store catalog.", productId));
        this.productId = productId;
    }

    public int getProductId() {
        return productId;
    }
}
