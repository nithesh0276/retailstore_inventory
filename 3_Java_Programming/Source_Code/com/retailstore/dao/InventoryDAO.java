package com.retailstore.dao;

import com.retailstore.exception.DatabaseOperationException;
import com.retailstore.model.Product;
import com.retailstore.model.StockUpdate;
import com.retailstore.util.DBConnection;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Data Access Object for real-time stock inspection and restocking.
 * Course: 25ITT32 Java Programming (Unit 4: Database Connection)
 */
public class InventoryDAO {

    public int getAvailableStock(int productId) {
        String sql = "SELECT available_stock FROM inventory WHERE product_id = ?;";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, productId);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt("available_stock");
                }
            }
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to check inventory stock: " + e.getMessage(), e);
        }
        return 0;
    }

    public boolean restockProduct(int productId, int additionalQuantity, String notes) {
        if (additionalQuantity <= 0) {
            throw new IllegalArgumentException("Restock quantity must be positive!");
        }
        String sql = "UPDATE inventory SET available_stock = available_stock + ?, last_updated = DATETIME('now', 'localtime') WHERE product_id = ?;";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, additionalQuantity);
            pstmt.setInt(2, productId);
            int affected = pstmt.executeUpdate();
            return affected > 0;
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to restock product: " + e.getMessage(), e);
        }
    }

    public List<Product> getLowStockProducts() {
        List<Product> list = new ArrayList<>();
        String sql = "SELECT product_id, product_name, category_name, available_stock, reorder_level FROM v_low_stock_alerts ORDER BY available_stock ASC;";
        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                Product p = new Product();
                p.setProductId(rs.getInt("product_id"));
                p.setProductName(rs.getString("product_name"));
                p.setCategoryName(rs.getString("category_name"));
                p.setAvailableStock(rs.getInt("available_stock"));
                p.setReorderLevel(rs.getInt("reorder_level"));
                list.add(p);
            }
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to query low stock alerts: " + e.getMessage(), e);
        }
        return list;
    }

    public List<StockUpdate> getRecentStockAudits(int limit) {
        List<StockUpdate> list = new ArrayList<>();
        String sql = """
            SELECT su.update_id, su.product_id, p.product_name, su.change_quantity,
                   su.update_type, su.balance_stock, su.update_timestamp, su.notes
            FROM stock_updates su
            JOIN products p ON su.product_id = p.product_id
            ORDER BY su.update_id DESC
            LIMIT ?;
        """;
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, limit);
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    StockUpdate su = new StockUpdate(
                        rs.getInt("update_id"),
                        rs.getInt("product_id"),
                        rs.getInt("change_quantity"),
                        rs.getString("update_type"),
                        rs.getInt("balance_stock"),
                        rs.getString("update_timestamp"),
                        rs.getString("notes")
                    );
                    su.setProductName(rs.getString("product_name"));
                    list.add(su);
                }
            }
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to query stock audits: " + e.getMessage(), e);
        }
        return list;
    }
}
