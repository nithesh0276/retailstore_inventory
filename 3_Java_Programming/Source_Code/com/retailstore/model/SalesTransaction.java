package com.retailstore.model;

import java.util.ArrayList;
import java.util.List;

/**
 * Master invoice transaction representing a customer checkout session.
 * Course: 25ITT32 Java Programming (Unit 1 & Unit 5: Collections)
 */
public class SalesTransaction {
    private int transactionId;
    private int customerId;
    private String customerName;
    private String transactionDate;
    private double totalAmount;
    private String paymentMode;
    private String cashierName;
    private List<SalesDetail> lineItems;

    public SalesTransaction() {
        this.lineItems = new ArrayList<>();
    }

    public SalesTransaction(int transactionId, int customerId, String transactionDate, double totalAmount, String paymentMode, String cashierName) {
        this.transactionId = transactionId;
        this.customerId = customerId;
        this.transactionDate = transactionDate;
        this.totalAmount = totalAmount;
        this.paymentMode = paymentMode;
        this.cashierName = cashierName;
        this.lineItems = new ArrayList<>();
    }

    public void addLineItem(SalesDetail item) {
        this.lineItems.add(item);
        this.totalAmount += item.getSubtotal();
    }

    public int getTransactionId() {
        return transactionId;
    }

    public void setTransactionId(int transactionId) {
        this.transactionId = transactionId;
    }

    public int getCustomerId() {
        return customerId;
    }

    public void setCustomerId(int customerId) {
        this.customerId = customerId;
    }

    public String getCustomerName() {
        return customerName;
    }

    public void setCustomerName(String customerName) {
        this.customerName = customerName;
    }

    public String getTransactionDate() {
        return transactionDate;
    }

    public void setTransactionDate(String transactionDate) {
        this.transactionDate = transactionDate;
    }

    public double getTotalAmount() {
        return totalAmount;
    }

    public void setTotalAmount(double totalAmount) {
        this.totalAmount = totalAmount;
    }

    public String getPaymentMode() {
        return paymentMode;
    }

    public void setPaymentMode(String paymentMode) {
        this.paymentMode = paymentMode;
    }

    public String getCashierName() {
        return cashierName;
    }

    public void setCashierName(String cashierName) {
        this.cashierName = cashierName;
    }

    public List<SalesDetail> getLineItems() {
        return lineItems;
    }

    public void setLineItems(List<SalesDetail> lineItems) {
        this.lineItems = lineItems;
    }

    @Override
    public String toString() {
        return String.format("Invoice #%d | Date: %s | Customer: %s | Total: $%.2f | Mode: %s",
                transactionId, transactionDate, customerName, totalAmount, paymentMode);
    }
}
