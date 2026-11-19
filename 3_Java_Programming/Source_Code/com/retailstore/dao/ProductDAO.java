package com.retailstore.dao;

import com.retailstore.exception.DatabaseOperationException;
import com.retailstore.model.Product;
import com.retailstore.util.DBConnection;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Data Access Object for Product catalog management.
 * Course: 25ITT32 Java Programming (Unit 4: Database Connection)
 */
public class ProductDAO {

    public List<Product> getAllProducts() {
        List<Product> list = new ArrayList<>();
        String sql = """
            SELECT p.product_id, p.product_name, p.category_id, c.category_name,
                   p.unit_price, p.cost_price, p.reorder_level, COALESCE(i.available_stock, 0) AS available_stock
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN inventory i ON p.product_id = i.product_id
            ORDER BY p.product_id;
        """;
        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                Product p = new Product(
                    rs.getInt("product_id"),
                    rs.getString("product_name"),
                    rs.getInt("category_id"),
                    rs.getDouble("unit_price"),
                    rs.getDouble("cost_price"),
                    rs.getInt("reorder_level")
                );
                p.setCategoryName(rs.getString("category_name"));
                p.setAvailableStock(rs.getInt("available_stock"));
                list.add(p);
            }
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to query products: " + e.getMessage(), e);
        }
        return list;
    }

    public Product getProductById(int productId) {
        String sql = """
            SELECT p.product_id, p.product_name, p.category_id, c.category_name,
                   p.unit_price, p.cost_price, p.reorder_level, COALESCE(i.available_stock, 0) AS available_stock
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            LEFT JOIN inventory i ON p.product_id = i.product_id
            WHERE p.product_id = ?;
        """;
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, productId);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    Product p = new Product(
                        rs.getInt("product_id"),
                        rs.getString("product_name"),
                        rs.getInt("category_id"),
                        rs.getDouble("unit_price"),
                        rs.getDouble("cost_price"),
                        rs.getInt("reorder_level")
                    );
                    p.setCategoryName(rs.getString("category_name"));
                    p.setAvailableStock(rs.getInt("available_stock"));
                    return p;
                }
            }
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to query product by ID: " + e.getMessage(), e);
        }
        return null;
    }

    public boolean addProductWithInitialStock(Product product, int initialStock) {
        Connection conn = DBConnection.getConnection();
        String insertProdSql = "INSERT INTO products (product_name, category_id, unit_price, cost_price, reorder_level) VALUES (?, ?, ?, ?, ?);";
        String insertInvSql = "INSERT INTO inventory (product_id, available_stock) VALUES (?, ?);";
        String insertAuditSql = "INSERT INTO stock_updates (product_id, change_quantity, update_type, balance_stock, notes) VALUES (?, ?, 'INITIAL', ?, 'New product catalog registration');";

        try {
            conn.setAutoCommit(false); // Begin ACID transaction
            int generatedProdId = -1;

            try (PreparedStatement pStmt = conn.prepareStatement(insertProdSql, Statement.RETURN_GENERATED_KEYS)) {
                pStmt.setString(1, product.getProductName());
                pStmt.setInt(2, product.getCategoryId());
                pStmt.setDouble(3, product.getUnitPrice());
                pStmt.setDouble(4, product.getCostPrice());
                pStmt.setInt(5, product.getReorderLevel());
                pStmt.executeUpdate();

                try (ResultSet rs = pStmt.getGeneratedKeys()) {
                    if (rs.next()) {
                        generatedProdId = rs.getInt(1);
                        product.setProductId(generatedProdId);
                    }
                }
            }

            if (generatedProdId > 0) {
                try (PreparedStatement invStmt = conn.prepareStatement(insertInvSql)) {
                    invStmt.setInt(1, generatedProdId);
                    invStmt.setInt(2, initialStock);
                    invStmt.executeUpdate();
                }

                try (PreparedStatement auditStmt = conn.prepareStatement(insertAuditSql)) {
                    auditStmt.setInt(1, generatedProdId);
                    auditStmt.setInt(2, initialStock);
                    auditStmt.setInt(3, initialStock);
                    auditStmt.executeUpdate();
                }
            }

            conn.commit(); // Commit transaction
            return true;
        } catch (SQLException e) {
            try {
                conn.rollback();
            } catch (SQLException rbEx) {
                System.err.println("Rollback failed: " + rbEx.getMessage());
            }
            throw new DatabaseOperationException("Transaction failed while adding product: " + e.getMessage(), e);
        } finally {
            try {
                conn.setAutoCommit(true);
            } catch (SQLException e) {
                System.err.println("Failed to reset auto-commit: " + e.getMessage());
            }
        }
    }
}
