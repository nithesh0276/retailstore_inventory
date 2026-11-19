package com.retailstore.model;

/**
 * Represents a retail product with pricing and reorder thresholds.
 * Course: 25ITT32 Java Programming (Unit 1: Classes & Methods)
 */
public class Product {
    private int productId;
    private String productName;
    private int categoryId;
    private String categoryName;
    private double unitPrice;
    private double costPrice;
    private int reorderLevel;
    private int availableStock;

    public Product() {}

    public Product(int productId, String productName, int categoryId, double unitPrice, double costPrice, int reorderLevel) {
        this.productId = productId;
        this.productName = productName;
        this.categoryId = categoryId;
        this.unitPrice = unitPrice;
        this.costPrice = costPrice;
        this.reorderLevel = reorderLevel;
    }

    public Product(String productName, int categoryId, double unitPrice, double costPrice, int reorderLevel) {
        this.productName = productName;
        this.categoryId = categoryId;
        this.unitPrice = unitPrice;
        this.costPrice = costPrice;
        this.reorderLevel = reorderLevel;
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

    public int getCategoryId() {
        return categoryId;
    }

    public void setCategoryId(int categoryId) {
        this.categoryId = categoryId;
    }

    public String getCategoryName() {
        return categoryName;
    }

    public void setCategoryName(String categoryName) {
        this.categoryName = categoryName;
    }

    public double getUnitPrice() {
        return unitPrice;
    }

    public void setUnitPrice(double unitPrice) {
        this.unitPrice = unitPrice;
    }

    public double getCostPrice() {
        return costPrice;
    }

    public void setCostPrice(double costPrice) {
        this.costPrice = costPrice;
    }

    public int getReorderLevel() {
        return reorderLevel;
    }

    public void setReorderLevel(int reorderLevel) {
        this.reorderLevel = reorderLevel;
    }

    public int getAvailableStock() {
        return availableStock;
    }

    public void setAvailableStock(int availableStock) {
        this.availableStock = availableStock;
    }

    public boolean isLowStock() {
        return availableStock <= reorderLevel;
    }

    @Override
    public String toString() {
        return String.format("[%2d] %-35s | Price: $%7.2f | Stock: %3d | Reorder: %2d",
                productId, productName, unitPrice, availableStock, reorderLevel);
    }
}
