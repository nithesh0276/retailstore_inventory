package com.retailstore.dao;

import com.retailstore.exception.DatabaseOperationException;
import com.retailstore.model.Customer;
import com.retailstore.util.DBConnection;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Data Access Object for Customer registry management.
 * Course: 25ITT32 Java Programming (Unit 4: Database Connection)
 */
public class CustomerDAO {

    public List<Customer> getAllCustomers() {
        List<Customer> list = new ArrayList<>();
        String sql = "SELECT customer_id, customer_name, phone, email, address FROM customers ORDER BY customer_id;";
        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                list.add(new Customer(
                    rs.getInt("customer_id"),
                    rs.getString("customer_name"),
                    rs.getString("phone"),
                    rs.getString("email"),
                    rs.getString("address")
                ));
            }
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to query customers: " + e.getMessage(), e);
        }
        return list;
    }

    public Customer getCustomerById(int customerId) {
        String sql = "SELECT customer_id, customer_name, phone, email, address FROM customers WHERE customer_id = ?;";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, customerId);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return new Customer(
                        rs.getInt("customer_id"),
                        rs.getString("customer_name"),
                        rs.getString("phone"),
                        rs.getString("email"),
                        rs.getString("address")
                    );
                }
            }
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to query customer by ID: " + e.getMessage(), e);
        }
        return null;
    }

    public boolean addCustomer(Customer customer) {
        String sql = "INSERT INTO customers (customer_name, phone, email, address) VALUES (?, ?, ?, ?);";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            pstmt.setString(1, customer.getCustomerName());
            pstmt.setString(2, customer.getPhone());
            pstmt.setString(3, customer.getEmail());
            pstmt.setString(4, customer.getAddress());
            int affected = pstmt.executeUpdate();
            if (affected > 0) {
                try (ResultSet rs = pstmt.getGeneratedKeys()) {
                    if (rs.next()) {
                        customer.setCustomerId(rs.getInt(1));
                    }
                }
                return true;
            }
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to register customer: " + e.getMessage(), e);
        }
        return false;
    }
}
