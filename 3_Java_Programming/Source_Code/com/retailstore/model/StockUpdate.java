package com.retailstore.model;

/**
 * Immutable audit ledger entry tracking stock movement events.
 * Course: 25ITT32 Java Programming (Unit 1: Classes)
 */
public class StockUpdate {
    private int updateId;
    private int productId;
    private String productName;
    private int changeQuantity;
    private String updateType;
    private int balanceStock;
    private String updateTimestamp;
    private String notes;

    public StockUpdate() {}

    public StockUpdate(int updateId, int productId, int changeQuantity, String updateType, int balanceStock, String updateTimestamp, String notes) {
        this.updateId = updateId;
        this.productId = productId;
        this.changeQuantity = changeQuantity;
        this.updateType = updateType;
        this.balanceStock = balanceStock;
        this.updateTimestamp = updateTimestamp;
        this.notes = notes;
    }

    public int getUpdateId() {
        return updateId;
    }

    public void setUpdateId(int updateId) {
        this.updateId = updateId;
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

    public int getChangeQuantity() {
        return changeQuantity;
    }

    public void setChangeQuantity(int changeQuantity) {
        this.changeQuantity = changeQuantity;
    }

    public String getUpdateType() {
        return updateType;
    }

    public void setUpdateType(String updateType) {
        this.updateType = updateType;
    }

    public int getBalanceStock() {
        return balanceStock;
    }

    public void setBalanceStock(int balanceStock) {
        this.balanceStock = balanceStock;
    }

    public String getUpdateTimestamp() {
        return updateTimestamp;
    }

    public void setUpdateTimestamp(String updateTimestamp) {
        this.updateTimestamp = updateTimestamp;
    }

    public String getNotes() {
        return notes;
    }

    public void setNotes(String notes) {
        this.notes = notes;
    }

    @Override
    public String toString() {
        return String.format("[%d] Prod #%d | Delta: %+d | Type: %-8s | Balance: %d | Time: %s",
                updateId, productId, changeQuantity, updateType, balanceStock, updateTimestamp);
    }
}
