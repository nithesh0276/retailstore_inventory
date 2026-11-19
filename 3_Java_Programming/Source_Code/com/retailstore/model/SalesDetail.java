package com.retailstore.model;

/**
 * Line item in a sales invoice.
 * Course: 25ITT32 Java Programming (Unit 1: Classes)
 */
public class SalesDetail {
    private int detailId;
    private int transactionId;
    private int productId;
    private String productName;
    private int quantitySold;
    private double unitPrice;
    private double subtotal;

    public SalesDetail() {}

    public SalesDetail(int detailId, int transactionId, int productId, int quantitySold, double unitPrice, double subtotal) {
        this.detailId = detailId;
        this.transactionId = transactionId;
        this.productId = productId;
        this.quantitySold = quantitySold;
        this.unitPrice = unitPrice;
        this.subtotal = subtotal;
    }

    public SalesDetail(int productId, int quantitySold, double unitPrice) {
        this.productId = productId;
        this.quantitySold = quantitySold;
        this.unitPrice = unitPrice;
        this.subtotal = quantitySold * unitPrice;
    }

    public int getDetailId() {
        return detailId;
    }

    public void setDetailId(int detailId) {
        this.detailId = detailId;
    }

    public int getTransactionId() {
        return transactionId;
    }

    public void setTransactionId(int transactionId) {
        this.transactionId = transactionId;
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

    public int getQuantitySold() {
        return quantitySold;
    }

    public void setQuantitySold(int quantitySold) {
        this.quantitySold = quantitySold;
    }

    public double getUnitPrice() {
        return unitPrice;
    }

    public void setUnitPrice(double unitPrice) {
        this.unitPrice = unitPrice;
    }

    public double getSubtotal() {
        return subtotal;
    }

    public void setSubtotal(double subtotal) {
        this.subtotal = subtotal;
    }

    @Override
    public String toString() {
        return String.format("Prod #%-2d | Qty: %2d | Unit Price: $%6.2f | Subtotal: $%7.2f",
                productId, quantitySold, unitPrice, subtotal);
    }
}
