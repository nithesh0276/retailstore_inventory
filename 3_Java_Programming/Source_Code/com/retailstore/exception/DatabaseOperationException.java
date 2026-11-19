package com.retailstore.exception;

/**
 * Custom runtime exception wrapping underlying SQL and JDBC transmission errors.
 * Course: 25ITT32 Java Programming (Unit 3: Exception Handling)
 */
public class DatabaseOperationException extends RuntimeException {
    public DatabaseOperationException(String message) {
        super(message);
    }

    public DatabaseOperationException(String message, Throwable cause) {
        super(message, cause);
    }
}
