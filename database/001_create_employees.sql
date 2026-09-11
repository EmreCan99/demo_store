-- Schema for the employees table
-- Run with: sqlite3 store.db < database/001_create_employees.sql

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    department TEXT,
    salary REAL
);