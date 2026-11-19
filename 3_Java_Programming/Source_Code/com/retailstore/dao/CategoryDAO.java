package com.retailstore.dao;

import com.retailstore.exception.DatabaseOperationException;
import com.retailstore.model.Category;
import com.retailstore.util.DBConnection;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

/**
 * Data Access Object for Category management.
 * Course: 25ITT32 Java Programming (Unit 4: Database Connection)
 */
public class CategoryDAO {

    public List<Category> getAllCategories() {
        List<Category> list = new ArrayList<>();
        String sql = "SELECT category_id, category_name, description FROM categories ORDER BY category_id;";
        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement();
             ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                list.add(new Category(
                    rs.getInt("category_id"),
                    rs.getString("category_name"),
                    rs.getString("description")
                ));
            }
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to query categories: " + e.getMessage(), e);
        }
        return list;
    }

    public Category getCategoryById(int categoryId) {
        String sql = "SELECT category_id, category_name, description FROM categories WHERE category_id = ?;";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, categoryId);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return new Category(
                        rs.getInt("category_id"),
                        rs.getString("category_name"),
                        rs.getString("description")
                    );
                }
            }
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to query category by ID: " + e.getMessage(), e);
        }
        return null;
    }

    public boolean addCategory(Category category) {
        String sql = "INSERT INTO categories (category_name, description) VALUES (?, ?);";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            pstmt.setString(1, category.getCategoryName());
            pstmt.setString(2, category.getDescription());
            int affected = pstmt.executeUpdate();
            if (affected > 0) {
                try (ResultSet rs = pstmt.getGeneratedKeys()) {
                    if (rs.next()) {
                        category.setCategoryId(rs.getInt(1));
                    }
                }
                return true;
            }
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to add category: " + e.getMessage(), e);
        }
        return false;
    }
}
