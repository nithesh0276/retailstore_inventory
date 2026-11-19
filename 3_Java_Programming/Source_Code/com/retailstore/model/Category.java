package com.retailstore.model;

/**
 * Represents a product category in the retail taxonomy.
 * Academic Regulation: VCET B.Tech IT (R2025) | Course: 25ITT32 Java Programming
 */
public class Category {
    private int categoryId;
    private String categoryName;
    private String description;

    public Category() {}

    public Category(int categoryId, String categoryName, String description) {
        this.categoryId = categoryId;
        this.categoryName = categoryName;
        this.description = description;
    }

    public Category(String categoryName, String description) {
        this.categoryName = categoryName;
        this.description = description;
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

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    @Override
    public String toString() {
        return String.format("[%d] %-22s - %s", categoryId, categoryName, description);
    }
}
