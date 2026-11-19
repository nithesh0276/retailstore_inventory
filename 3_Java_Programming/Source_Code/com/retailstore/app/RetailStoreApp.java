package com.retailstore.app;

import com.retailstore.dao.CategoryDAO;
import com.retailstore.dao.CustomerDAO;
import com.retailstore.dao.ProductDAO;
import com.retailstore.exception.InsufficientStockException;
import com.retailstore.exception.ProductNotFoundException;
import com.retailstore.model.Category;
import com.retailstore.model.Customer;
import com.retailstore.model.Product;
import com.retailstore.model.SalesDetail;
import com.retailstore.service.InventoryService;
import com.retailstore.service.ReportService;
import com.retailstore.service.SalesService;
import com.retailstore.util.ConsoleFormatter;
import com.retailstore.util.DBConnection;

import java.util.*;

/**
 * Interactive Console Management Dashboard for the Retail Store System.
 * Academic Regulation: VCET B.Tech IT (R2025) | Course: 25ITT32 Java Programming
 */
public class RetailStoreApp {
    private final ProductDAO productDAO;
    private final CategoryDAO categoryDAO;
    private final CustomerDAO customerDAO;
    private final SalesService salesService;
    private final InventoryService inventoryService;
    private final ReportService reportService;
    private final Scanner scanner;

    public RetailStoreApp() {
        this.productDAO = new ProductDAO();
        this.categoryDAO = new CategoryDAO();
        this.customerDAO = new CustomerDAO();
        this.salesService = new SalesService();
        this.inventoryService = new InventoryService();
        this.reportService = new ReportService();
        this.scanner = new Scanner(System.in);
    }

    public void run() {
        while (true) {
            ConsoleFormatter.printHeader("RETAIL STORE INVENTORY & SALES SYSTEM - DASHBOARD");
            System.out.println(" 1. View Product Catalog & Inventory Availability");
            System.out.println(" 2. Register New Product in Catalog");
            System.out.println(" 3. View Registered Product Categories");
            System.out.println(" 4. View Customer Directory");
            System.out.println(" 5. Check Real-Time Stock Availability");
            System.out.println(" 6. Process Sales Transaction (Checkout)");
            System.out.println(" 7. Test Over-Sale Prevention Logic");
            System.out.println(" 8. Restock Product Inventory");
            System.out.println(" 9. Generate Daily Sales Report");
            System.out.println("10. Generate Low-Stock Alert Report");
            System.out.println("11. View Stock Movement Audit Ledger");
            System.out.println("12. Run Full Automated System Demonstration");
            System.out.println(" 0. Exit System");
            ConsoleFormatter.printDivider();
            System.out.print("Enter your choice (0-12): ");

            String input = scanner.nextLine().trim();
            if ("0".equals(input)) {
                ConsoleFormatter.printSuccess("Exiting Retail Store System. Goodbye!");
                DBConnection.closeConnection();
                break;
            }

            try {
                int choice = Integer.parseInt(input);
                handleChoice(choice);
            } catch (NumberFormatException e) {
                ConsoleFormatter.printError("Invalid input! Please enter a numeric choice between 0 and 12.");
            } catch (Exception e) {
                ConsoleFormatter.printError("An error occurred: " + e.getMessage());
            }

            System.out.println("\nPress [ENTER] to return to the main menu...");
            scanner.nextLine();
        }
    }

    private void handleChoice(int choice) throws Exception {
        switch (choice) {
            case 1 -> viewProductCatalog();
            case 2 -> registerNewProduct();
            case 3 -> viewCategories();
            case 4 -> viewCustomers();
            case 5 -> checkProductStock();
            case 6 -> processSaleInteractive();
            case 7 -> testOverSalePrevention();
            case 8 -> restockProductInteractive();
            case 9 -> generateDailySalesReport();
            case 10 -> generateLowStockReport();
            case 11 -> viewStockAuditLedger();
            case 12 -> AutomatedDemoRunner.runFullDemo();
            default -> ConsoleFormatter.printError("Invalid choice! Please select an option between 0 and 12.");
        }
    }

    private void viewProductCatalog() {
        ConsoleFormatter.printSubHeader("PRODUCT CATALOG & INVENTORY AVAILABILITY REPORT");
        List<Product> products = reportService.getProductAvailabilityReport();
        System.out.printf("%-4s | %-32s | %-18s | %-10s | %-8s | %-9s%n",
                "ID", "PRODUCT NAME", "CATEGORY", "PRICE ($)", "STOCK", "REORDER");
        ConsoleFormatter.printDivider();
        for (Product p : products) {
            System.out.printf("%-4d | %-32s | %-18s | %10.2f | %8d | %9d%n",
                    p.getProductId(), p.getProductName(), p.getCategoryName(),
                    p.getUnitPrice(), p.getAvailableStock(), p.getReorderLevel());
        }
        System.out.printf("%nTotal Inventory Valuation: $%,.2f%n", reportService.getTotalInventoryValuation());
    }

    private void registerNewProduct() {
        ConsoleFormatter.printSubHeader("REGISTER NEW PRODUCT IN CATALOG");
        System.out.print("Enter Product Name: ");
        String name = scanner.nextLine().trim();
        System.out.print("Enter Category ID (1:Electronics, 2:Groceries, 3:Beverages, 4:Personal, 5:Home): ");
        int catId = Integer.parseInt(scanner.nextLine().trim());
        System.out.print("Enter Unit Selling Price ($): ");
        double price = Double.parseDouble(scanner.nextLine().trim());
        System.out.print("Enter Cost Procurement Price ($): ");
        double cost = Double.parseDouble(scanner.nextLine().trim());
        System.out.print("Enter Reorder Threshold Level: ");
        int reorder = Integer.parseInt(scanner.nextLine().trim());
        System.out.print("Enter Initial Stock Units: ");
        int stock = Integer.parseInt(scanner.nextLine().trim());

        Product product = new Product(name, catId, price, cost, reorder);
        boolean success = productDAO.addProductWithInitialStock(product, stock);
        if (success) {
            ConsoleFormatter.printSuccess("Product '" + name + "' registered successfully with ID #" + product.getProductId());
        } else {
            ConsoleFormatter.printError("Failed to register product.");
        }
    }

    private void viewCategories() {
        ConsoleFormatter.printSubHeader("PRODUCT CATEGORIES");
        List<Category> list = categoryDAO.getAllCategories();
        for (Category c : list) {
            System.out.println(c);
        }
    }

    private void viewCustomers() {
        ConsoleFormatter.printSubHeader("CUSTOMER DIRECTORY");
        List<Customer> list = customerDAO.getAllCustomers();
        for (Customer c : list) {
            System.out.println(c);
        }
    }

    private void checkProductStock() throws ProductNotFoundException {
        ConsoleFormatter.printSubHeader("CHECK REAL-TIME STOCK AVAILABILITY");
        System.out.print("Enter Product ID: ");
        int prodId = Integer.parseInt(scanner.nextLine().trim());
        Product p = productDAO.getProductById(prodId);
        if (p == null) {
            throw new ProductNotFoundException(prodId);
        }
        int stock = inventoryService.checkStock(prodId);
        System.out.println("Product Name    : " + p.getProductName());
        System.out.println("Category        : " + p.getCategoryName());
        System.out.println("Unit Price      : $" + String.format("%.2f", p.getUnitPrice()));
        System.out.println("Available Stock : " + stock + " units");
        System.out.println("Reorder Level   : " + p.getReorderLevel() + " units");
        if (stock <= p.getReorderLevel()) {
            ConsoleFormatter.printWarning("STATUS: LOW STOCK WARNING! Restocking recommended.");
        } else {
            ConsoleFormatter.printSuccess("STATUS: Adequate stock on shelf.");
        }
    }

    private void processSaleInteractive() {
        ConsoleFormatter.printSubHeader("PROCESS SALES TRANSACTION (CHECKOUT)");
        try {
            System.out.print("Enter Customer ID (1-10): ");
            int custId = Integer.parseInt(scanner.nextLine().trim());
            System.out.print("Enter Product ID to purchase: ");
            int prodId = Integer.parseInt(scanner.nextLine().trim());
            System.out.print("Enter Quantity to purchase: ");
            int qty = Integer.parseInt(scanner.nextLine().trim());
            System.out.print("Enter Payment Mode (Cash/Credit Card/Debit Card/UPI): ");
            String mode = scanner.nextLine().trim();

            List<SalesDetail> items = new ArrayList<>();
            items.add(new SalesDetail(prodId, qty, 0.0));

            int txId = salesService.processSale(custId, items, mode, "CounterOperator");
            ConsoleFormatter.printSuccess("Transaction #" + txId + " processed successfully! Stock decremented automatically.");
        } catch (InsufficientStockException e) {
            ConsoleFormatter.printError("CHECKOUT REJECTED: " + e.getMessage());
        } catch (Exception e) {
            ConsoleFormatter.printError("Sales processing error: " + e.getMessage());
        }
    }

    private void testOverSalePrevention() {
        ConsoleFormatter.printSubHeader("TEST OVER-SALE PREVENTION DEFENSE");
        System.out.println("Testing over-sale rejection by attempting to purchase 500 units of Product #4...");
        try {
            List<SalesDetail> items = new ArrayList<>();
            items.add(new SalesDetail(4, 500, 129.99));
            salesService.processSale(1, items, "Credit Card", "TestRunner");
            ConsoleFormatter.printError("TEST FAILED: System permitted over-sale!");
        } catch (InsufficientStockException e) {
            ConsoleFormatter.printSuccess("OVER-SALE BLOCKED AS EXPECTED!");
            System.out.println("Intercepted Exception: " + e.getMessage());
            System.out.println("Available Stock: " + e.getAvailableStock() + " units | Requested: " + e.getRequestedQuantity() + " units");
        } catch (Exception e) {
            ConsoleFormatter.printError("Unexpected error: " + e.getMessage());
        }
    }

    private void restockProductInteractive() {
        ConsoleFormatter.printSubHeader("RESTOCK PRODUCT INVENTORY");
        try {
            System.out.print("Enter Product ID: ");
            int prodId = Integer.parseInt(scanner.nextLine().trim());
            System.out.print("Enter Quantity to add to stock: ");
            int qty = Integer.parseInt(scanner.nextLine().trim());
            System.out.print("Enter Restock Notes: ");
            String notes = scanner.nextLine().trim();

            boolean ok = inventoryService.restockProduct(prodId, qty, notes);
            if (ok) {
                int newStock = inventoryService.checkStock(prodId);
                ConsoleFormatter.printSuccess("Product #" + prodId + " restocked successfully! New Stock: " + newStock + " units");
            } else {
                ConsoleFormatter.printError("Failed to restock product.");
            }
        } catch (Exception e) {
            ConsoleFormatter.printError("Restock error: " + e.getMessage());
        }
    }

    private void generateDailySalesReport() {
        ConsoleFormatter.printSubHeader("DAILY SALES REVENUE REPORT (JAVA STREAM API)");
        Map<String, Double> summary = reportService.getDailySalesSummary();
        System.out.printf("%-15s | %-15s%n", "SALE DATE", "DAILY REVENUE ($)");
        ConsoleFormatter.printDivider();
        double grandTotal = 0.0;
        for (Map.Entry<String, Double> entry : summary.entrySet()) {
            System.out.printf("%-15s | %15.2f%n", entry.getKey(), entry.getValue());
            grandTotal += entry.getValue();
        }
        ConsoleFormatter.printDivider();
        System.out.printf("%-15s | %15.2f%n", "CUMULATIVE TOTAL", grandTotal);
    }

    private void generateLowStockReport() {
        ConsoleFormatter.printSubHeader("LOW-STOCK ALERT REPORT (PRODUCTS AT OR BELOW REORDER LEVEL)");
        List<Product> lowStock = reportService.getLowStockReport();
        if (lowStock.isEmpty()) {
            ConsoleFormatter.printSuccess("All products have adequate stock levels!");
            return;
        }
        System.out.printf("%-4s | %-32s | %-18s | %-8s | %-9s | %-12s%n",
                "ID", "PRODUCT NAME", "CATEGORY", "STOCK", "REORDER", "DEFICIT");
        ConsoleFormatter.printDivider();
        for (Product p : lowStock) {
            int deficit = p.getReorderLevel() - p.getAvailableStock();
            System.out.printf("%-4d | %-32s | %-18s | %8d | %9d | %12d%n",
                    p.getProductId(), p.getProductName(), p.getCategoryName(),
                    p.getAvailableStock(), p.getReorderLevel(), deficit);
        }
    }

    private void viewStockAuditLedger() {
        ConsoleFormatter.printSubHeader("RECENT STOCK MOVEMENT AUDIT LEDGER (LAST 10 EVENTS)");
        var audits = inventoryService.getAuditLog(10);
        for (var a : audits) {
            System.out.println(a);
        }
    }

    public static void main(String[] args) {
        RetailStoreApp app = new RetailStoreApp();
        app.run();
    }
}
