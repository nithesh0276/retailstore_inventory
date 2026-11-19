package com.retailstore.service;

import com.retailstore.dao.ProductDAO;
import com.retailstore.dao.SalesDAO;
import com.retailstore.model.Product;
import com.retailstore.model.SalesTransaction;

import java.util.*;
import java.util.stream.Collectors;

/**
 * Report generation engine powered by Java 8+ Stream API and Lambda Expressions.
 * Course: 25ITT32 Java Programming (Unit 5: Lambdas and Streams API)
 */
public class ReportService {
    private final ProductDAO productDAO;
    private final SalesDAO salesDAO;

    public ReportService() {
        this.productDAO = new ProductDAO();
        this.salesDAO = new SalesDAO();
    }

    /**
     * Report 1: Real-time Product Availability Report.
     */
    public List<Product> getProductAvailabilityReport() {
        List<Product> products = productDAO.getAllProducts();
        // Sort by Category Name and then Product Name using Stream API
        return products.stream()
                .sorted(Comparator.comparing(Product::getCategoryName)
                        .thenComparing(Product::getProductName))
                .collect(Collectors.toList());
    }

    /**
     * Report 2: Low-Stock Items Report.
     * Filters items where available stock <= reorder level using Stream filter().
     */
    public List<Product> getLowStockReport() {
        List<Product> products = productDAO.getAllProducts();
        return products.stream()
                .filter(Product::isLowStock)
                .sorted(Comparator.comparingInt(Product::getAvailableStock))
                .collect(Collectors.toList());
    }

    /**
     * Report 3: Daily Sales Revenue Aggregation using Stream Collectors.groupingBy.
     */
    public Map<String, Double> getDailySalesSummary() {
        List<SalesTransaction> transactions = salesDAO.getAllTransactions();
        return transactions.stream()
                .collect(Collectors.groupingBy(
                        tx -> tx.getTransactionDate().substring(0, 10),
                        TreeMap::new,
                        Collectors.summingDouble(SalesTransaction::getTotalAmount)
                ));
    }

    /**
     * Report 4: Total Inventory Valuation using Stream mapToDouble and sum().
     */
    public double getTotalInventoryValuation() {
        List<Product> products = productDAO.getAllProducts();
        return products.stream()
                .mapToDouble(p -> p.getUnitPrice() * p.getAvailableStock())
                .sum();
    }
}
