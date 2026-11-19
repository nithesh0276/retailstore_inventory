package com.retailstore.util;

/**
 * Utility for formatting console output with clean Unicode/ASCII borders and tables.
 * Course: 25ITT32 Java Programming (Unit 1: Console I/O)
 */
public class ConsoleFormatter {
    public static final String RESET  = "\u001B[0m";
    public static final String BLACK  = "\u001B[30m";
    public static final String RED    = "\u001B[31m";
    public static final String GREEN  = "\u001B[32m";
    public static final String YELLOW = "\u001B[33m";
    public static final String BLUE   = "\u001B[34m";
    public static final String PURPLE = "\u001B[35m";
    public static final String CYAN   = "\u001B[36m";
    public static final String WHITE  = "\u001B[37m";
    public static final String BOLD   = "\u001B[1m";

    public static void printHeader(String title) {
        int width = 80;
        String line = "=".repeat(width);
        System.out.println(CYAN + BOLD + line + RESET);
        int pad = (width - title.length() - 2) / 2;
        String padStr = " ".repeat(Math.max(0, pad));
        System.out.println(CYAN + BOLD + padStr + title + RESET);
        System.out.println(CYAN + BOLD + line + RESET);
    }

    public static void printSubHeader(String subtitle) {
        System.out.println("\n" + YELLOW + BOLD + ">>> " + subtitle + RESET);
        System.out.println("-".repeat(75));
    }

    public static void printSuccess(String message) {
        System.out.println(GREEN + BOLD + "[SUCCESS] " + message + RESET);
    }

    public static void printWarning(String message) {
        System.out.println(YELLOW + BOLD + "[WARNING] " + message + RESET);
    }

    public static void printError(String message) {
        System.out.println(RED + BOLD + "[ERROR] " + message + RESET);
    }

    public static void printDivider() {
        System.out.println("-".repeat(80));
    }
}
