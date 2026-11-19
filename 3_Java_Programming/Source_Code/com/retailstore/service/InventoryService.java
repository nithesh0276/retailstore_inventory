package com.retailstore.service;

import com.retailstore.dao.InventoryDAO;
import com.retailstore.dao.ProductDAO;
import com.retailstore.exception.ProductNotFoundException;
import com.retailstore.model.Product;
import com.retailstore.model.StockUpdate;

import java.util.List;

/**
 * Service managing stock availability queries, low-stock threshold alerting, and replenishment.
 * Course: 25ITT32 Java Programming (Unit 2 & Unit 5)
 */
public class InventoryService {
    private final InventoryDAO inventoryDAO;
    private final ProductDAO productDAO;

    public InventoryService() {
        this.inventoryDAO = new InventoryDAO();
        this.productDAO = new ProductDAO();
    }

    public int checkStock(int productId) throws ProductNotFoundException {
        Product p = productDAO.getProductById(productId);
        if (p == null) {
            throw new ProductNotFoundException(productId);
        }
        return inventoryDAO.getAvailableStock(productId);
    }

    public boolean restockProduct(int productId, int quantity, String notes) throws ProductNotFoundException {
        Product p = productDAO.getProductById(productId);
        if (p == null) {
            throw new ProductNotFoundException(productId);
        }
        return inventoryDAO.restockProduct(productId, quantity, notes);
    }

    public List<Product> getLowStockAlerts() {
        return inventoryDAO.getLowStockProducts();
    }

    public List<StockUpdate> getAuditLog(int limit) {
        return inventoryDAO.getRecentStockAudits(limit);
    }
}
