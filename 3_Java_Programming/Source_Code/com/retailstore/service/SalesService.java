package com.retailstore.service;

import com.retailstore.dao.CustomerDAO;
import com.retailstore.dao.InventoryDAO;
import com.retailstore.dao.ProductDAO;
import com.retailstore.dao.SalesDAO;
import com.retailstore.exception.InsufficientStockException;
import com.retailstore.exception.ProductNotFoundException;
import com.retailstore.model.Customer;
import com.retailstore.model.Product;
import com.retailstore.model.SalesDetail;
import com.retailstore.model.SalesTransaction;

import java.util.List;

/**
 * Core business service orchestrating point-of-sale checkout and stock enforcement.
 * Course: 25ITT32 Java Programming (Unit 3: Exception Handling & Unit 5: Collections)
 */
public class SalesService {
    private final ProductDAO productDAO;
    private final InventoryDAO inventoryDAO;
    private final SalesDAO salesDAO;
    private final CustomerDAO customerDAO;

    public SalesService() {
        this.productDAO = new ProductDAO();
        this.inventoryDAO = new InventoryDAO();
        this.salesDAO = new SalesDAO();
        this.customerDAO = new CustomerDAO();
    }

    /**
     * Validates stock availability for an item.
     * @throws InsufficientStockException if requested quantity exceeds available stock.
     */
    public void validateStockAvailability(int productId, int requestedQuantity)
            throws InsufficientStockException, ProductNotFoundException {
        if (requestedQuantity <= 0) {
            throw new IllegalArgumentException("Requested quantity must be strictly greater than zero!");
        }

        Product product = productDAO.getProductById(productId);
        if (product == null) {
            throw new ProductNotFoundException(productId);
        }

        int availableStock = inventoryDAO.getAvailableStock(productId);
        if (requestedQuantity > availableStock) {
            throw new InsufficientStockException(
                "SALE BLOCKED: Requested quantity exceeds available inventory stock!",
                productId,
                product.getProductName(),
                availableStock,
                requestedQuantity
            );
        }
    }

    /**
     * Executes a complete sales transaction with atomic stock deduction and over-sale guard.
     */
    public int processSale(int customerId, List<SalesDetail> items, String paymentMode, String cashierName)
            throws InsufficientStockException, ProductNotFoundException {
        if (items == null || items.isEmpty()) {
            throw new IllegalArgumentException("Cart cannot be empty for sales processing!");
        }

        Customer customer = customerDAO.getCustomerById(customerId);
        if (customer == null) {
            throw new IllegalArgumentException("Customer with ID " + customerId + " does not exist!");
        }

        // STEP 1: Pre-validate stock availability for ALL line items before initiating write
        for (SalesDetail item : items) {
            validateStockAvailability(item.getProductId(), item.getQuantitySold());
            
            // Populate unit price and subtotal from catalog to guarantee pricing consistency
            Product p = productDAO.getProductById(item.getProductId());
            item.setUnitPrice(p.getUnitPrice());
            item.setSubtotal(p.getUnitPrice() * item.getQuantitySold());
            item.setProductName(p.getProductName());
        }

        // STEP 2: Assemble master sales transaction
        SalesTransaction tx = new SalesTransaction();
        tx.setCustomerId(customerId);
        tx.setCustomerName(customer.getCustomerName());
        tx.setPaymentMode(paymentMode);
        tx.setCashierName(cashierName);
        for (SalesDetail item : items) {
            tx.addLineItem(item);
        }

        // STEP 3: Persist transaction via DAO (Database triggers handle atomic stock deduction)
        int txId = salesDAO.recordTransaction(tx);
        return txId;
    }
}
