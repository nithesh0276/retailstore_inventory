package com.retailstore.model;

/**
 * Represents on-hand stock and physical inventory balance for a product.
 * Course: 25ITT32 Java Programming (Unit 1: Classes & Encapsulation)
 */
public class Inventory {
    private int inventoryId;
    private int productId;
    private String productName;
    private int availableStock;
    private String lastUpdated;

    public Inventory() {}

    public Inventory(int inventoryId, int productId, int availableStock, String lastUpdated) {
        this.inventoryId = inventoryId;
        this.productId = productId;
        this.availableStock = availableStock;
        this.lastUpdated = lastUpdated;
    }

    public int getInventoryId() {
        return inventoryId;
    }

    public void setInventoryId(int inventoryId) {
        this.inventoryId = inventoryId;
    }

    public int getProductId() {
        return productId;
    }

    public void setProductId(int productId) {
        this.productId = productId;
    }

    public String getProductName() {
        return productName;
    }

    public void setProductName(String productName) {
        this.productName = productName;
    }

    public int getAvailableStock() {
        return availableStock;
    }

    public void setAvailableStock(int availableStock) {
        this.availableStock = availableStock;
    }

    public String getLastUpdated() {
        return lastUpdated;
    }

    public void setLastUpdated(String lastUpdated) {
        this.lastUpdated = lastUpdated;
    }

    @Override
    public String toString() {
        return String.format("Inventory[ID=%d, ProdId=%d, Stock=%d, LastUpdated=%s]",
                inventoryId, productId, availableStock, lastUpdated);
    }
}
