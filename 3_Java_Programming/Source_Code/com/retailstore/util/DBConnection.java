package com.retailstore.util;

import com.retailstore.exception.DatabaseOperationException;

import java.io.File;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

/**
 * Singleton JDBC Connection Provider for SQLite.
 * Course: 25ITT32 Java Programming (Unit 4: Database Connection)
 */
public class DBConnection {
    private static Connection connection = null;

    private DBConnection() {}

    /**
     * Resolves the absolute path to retail_store.db across diverse directory executions.
     */
    private static String resolveDatabasePath() {
        String[] potentialPaths = {
            "retail_store.db",
            "../retail_store.db",
            "../../retail_store.db",
            "../2_Database_Management_System/retail_store.db",
            "2_Database_Management_System/retail_store.db",
            "d:/nithe/retail store inventory/Retail_Store_Inventory_and_Sales_Analysis_System/2_Database_Management_System/retail_store.db",
            "d:/nithe/retail store inventory/Retail_Store_Inventory_and_Sales_Analysis_System/retail_store.db"
        };

        for (String p : potentialPaths) {
            File f = new File(p);
            if (f.exists() && f.isFile()) {
                return f.getAbsolutePath();
            }
        }
        return "retail_store.db"; // fallback
    }

    public static synchronized Connection getConnection() {
        try {
            if (connection == null || connection.isClosed()) {
                // Load SQLite JDBC Driver
                Class.forName("org.sqlite.JDBC");
                String dbFile = resolveDatabasePath();
                String jdbcUrl = "jdbc:sqlite:" + dbFile;
                connection = DriverManager.getConnection(jdbcUrl);
                
                // Enforce foreign key constraints in SQLite
                try (var stmt = connection.createStatement()) {
                    stmt.execute("PRAGMA foreign_keys = ON;");
                }
            }
        } catch (ClassNotFoundException e) {
            throw new DatabaseOperationException("SQLite JDBC Driver not found in classpath. Ensure sqlite-jdbc.jar is provided in lib/", e);
        } catch (SQLException e) {
            throw new DatabaseOperationException("Failed to establish SQLite database connection: " + e.getMessage(), e);
        }
        return connection;
    }

    public static synchronized void closeConnection() {
        try {
            if (connection != null && !connection.isClosed()) {
                connection.close();
            }
        } catch (SQLException e) {
            System.err.println("Error closing database connection: " + e.getMessage());
        }
    }
}
