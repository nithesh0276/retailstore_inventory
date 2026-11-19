package com.retailstore.dao;

import com.retailstore.exception.DatabaseOperationException;
import com.retailstore.model.SalesDetail;
import com.retailstore.model.SalesTransaction;
import com.retailstore.util.DBConnection;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Data Access Object for Sales Transaction recording with ACID transaction control.
 * Course: 25ITT32 Java Programming (Unit 4: Database Connection)
 */
public class SalesDAO {

    public int recordTransaction(SalesTransaction tx) {
        Connection conn = DBConnection.getConnection();
        String insertTxSql = "INSERT INTO sales_transactions (customer_id, transaction_date, total_amount, payment_mode, cashier_name) VALUES (?, ?, ?, ?, ?);";
        String insertDetailSql = "INSERT INTO sales_details (transaction_id, product_id, quantity_sold, unit_price, subtotal) VALUES (?, ?, ?, ?, ?);";

        try {
            conn.setAutoCommit(false); // Begin ACID boundary
            int generatedTxId = -1;

            try (PreparedStatement txStmt = conn.prepareStatement(insertTxSql, Statement.RETURN_GENERATED_KEYS)) {
                txStmt.setInt(1, tx.getCustomerId());
                txStmt.setString(2, tx.getTransactionDate() != null ? tx.getTransactionDate() : "CURRENT_TIMESTAMP");
                txStmt.setDouble(3, tx.getTotalAmount());
                txStmt.setString(4, tx.getPaymentMode());
                txStmt.setString(5, tx.getCashierName());
                txStmt.executeUpdate();

                try (ResultSet rs = txStmt.getGeneratedKeys()) {
                    if (rs.next()) {
                        generatedTxId = rs.getInt(1);
                        tx.setTransactionId(generatedTxId);
                    }
                }
            }

            if (generatedTxId > 0) {
                try (PreparedStatement dStmt = conn.prepareStatement(insertDetailSql, Statement.RETURN_GENERATED_KEYS)) {
                    for (SalesDetail detail : tx.getLineItems()) {
                        dStmt.setInt(1, generatedTxId);
                        dStmt.setInt(2, detail.getProductId());
                        dStmt.setInt(3, detail.getQuantitySold());
                        dStmt.setDouble(4, detail.getUnitPrice());
                        dStmt.setDouble(5, detail.getSubtotal());
                        dStmt.executeUpdate();
                        
                        try (ResultSet rs = dStmt.getGeneratedKeys()) {
                            if (rs.next()) {
                                detail.setDetailId(rs.getInt(1));
                            }
                        }
                    }
                }
            }

            conn.commit(); // Commit atomic transaction
            return generatedTxId;
        } catch (SQLException e) {
            try {
                conn.rollback();
            } catch (SQLException rbEx) {
                System.err.println("Transaction Rollback Failed: " + rbEx.getMessage());
            }
            throw new DatabaseOperationException("Failed to persist sales transaction: " + e.getMessage(), e);
        } finally {
            try {
                conn.setAutoCommit(true);
            } catch (SQLException e) {
                System.err.println("Failed to reset auto-commit: " + e.getMessage());
            }
        }
    }

    public List<SalesTransaction> getAllTransactions() {
        List<SalesTransaction> list = new ArrayList<>();
        String sql = """
            SELECT st.transaction_id, st.customer_id, c.customer_name,
                   st.transaction_date, st.total_amount, st.payment_mode, st.cashier_name
            FROM sales_transactions st
            JOIN customers c ON st.customer_id = c.customer_id
            ORDER BY st.transaction_id DESC;
        """;
        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                SalesTransaction tx = new SalesTransaction(
                    rs.getInt("transaction_id"),
                    rs.getInt("customer_id"),
                    rs.getString("transaction_date"),
                    rs.getDouble("total_amount"),
                    rs.getString("payment_mode"),
                    rs.getString("cashier_name")
                );
                tx.setCustomerName(rs.getString("customer_name"));
                list.add(tx);
            }
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to query sales transactions: " + e.getMessage(), e);
        }
        return list;
    }
}
