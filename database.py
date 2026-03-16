"""
Database operations for Student Expense Tracker
SQLite database for storing expenses and categories
"""

import sqlite3
from pathlib import Path
from config import DB_FILE, DEFAULT_CATEGORIES, DATE_FORMAT
from datetime import datetime

def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(str(DB_FILE))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with schema."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Create categories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                color TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category_id INTEGER NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        ''')
        
        # Create budget table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER NOT NULL,
                month INTEGER NOT NULL,
                year INTEGER NOT NULL,
                limit REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(category_id, month, year),
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        ''')
        
        # Insert default categories if empty
        cursor.execute("SELECT COUNT(*) FROM categories")
        if cursor.fetchone()[0] == 0:
            for cat in DEFAULT_CATEGORIES:
                cursor.execute(
                    "INSERT INTO categories (name, color) VALUES (?, ?)",
                    (cat['name'], cat['color'])
                )
        
        conn.commit()
        print("Database initialized successfully")
        
    except Exception as e:
        print(f"Database initialization error: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

def get_categories():
    """Get all categories."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, name, color FROM categories ORDER BY name")
        return cursor.fetchall()
    finally:
        conn.close()

def add_expense(date, amount, category_id, description=""):
    """Add new expense."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO expenses (date, amount, category_id, description) VALUES (?, ?, ?, ?)",
            (date, amount, category_id, description)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding expense: {str(e)}")
        return False
    finally:
        conn.close()

def update_expense(expense_id, date, amount, category_id, description=""):
    """Update existing expense."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE expenses SET date=?, amount=?, category_id=?, description=? WHERE id=?",
            (date, amount, category_id, description, expense_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating expense: {str(e)}")
        return False
    finally:
        conn.close()

def delete_expense(expense_id):
    """Delete expense."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting expense: {str(e)}")
        return False
    finally:
        conn.close()

def get_expenses(start_date=None, end_date=None, category_id=None):
    """Get expenses with optional filtering."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT e.id, e.date, e.amount, e.category_id, e.description,
                   c.name as category_name, c.color
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            WHERE 1=1
        """
        params = []
        
        if start_date:
            query += " AND e.date >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND e.date <= ?"
            params.append(end_date)
        
        if category_id:
            query += " AND e.category_id = ?"
            params.append(category_id)
        
        query += " ORDER BY e.date DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        conn.close()

def get_category_summary(start_date=None, end_date=None):
    """Get spending summary by category."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
            SELECT c.id, c.name, c.color, SUM(e.amount) as total
            FROM categories c
            LEFT JOIN expenses e ON c.id = e.category_id
        """
        params = []
        
        if start_date or end_date:
            query += " WHERE 1=1"
            if start_date:
                query += " AND e.date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND e.date <= ?"
                params.append(end_date)
        
        query += " GROUP BY c.id, c.name, c.color ORDER BY total DESC"
        
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        conn.close()

def set_budget(category_id, month, year, limit):
    """Set budget for category."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT OR REPLACE INTO budgets (category_id, month, year, limit)
               VALUES (?, ?, ?, ?)""",
            (category_id, month, year, limit)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error setting budget: {str(e)}")
        return False
    finally:
        conn.close()

def get_budget(category_id, month, year):
    """Get budget for category."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT limit FROM budgets 
               WHERE category_id=? AND month=? AND year=?""",
            (category_id, month, year)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()

def get_all_budgets():
    """Get all budgets."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT b.id, b.category_id, c.name, c.color, b.month, b.year, b.limit
            FROM budgets b
            JOIN categories c ON b.category_id = c.id
            ORDER BY b.year DESC, b.month DESC
        """)
        return cursor.fetchall()
    finally:
        conn.close()
