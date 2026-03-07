"""
Database module - SQLite connection and table management
"""

import sqlite3
from typing import Optional

DB_NAME = "poultry_farm.db"

def get_connection() -> sqlite3.Connection:
    """Get database connection"""
    return sqlite3.connect(DB_NAME)

def init_db():
    """Initialize database with all required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Daily entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            mortality INTEGER DEFAULT 0,
            production INTEGER DEFAULT 0,
            eggs_sold INTEGER DEFAULT 0,
            egg_price REAL DEFAULT 0.0,
            notes TEXT
        )
    ''')
    
    # Add missing columns if they don't exist (for existing databases)
    try:
        cursor.execute('SELECT eggs_sold FROM daily_entries LIMIT 1')
    except sqlite3.OperationalError:
        cursor.execute('ALTER TABLE daily_entries ADD COLUMN eggs_sold INTEGER DEFAULT 0')
    
    try:
        cursor.execute('SELECT egg_price FROM daily_entries LIMIT 1')
    except sqlite3.OperationalError:
        cursor.execute('ALTER TABLE daily_entries ADD COLUMN egg_price REAL DEFAULT 0')
    
    # Expenses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL,
            description TEXT
        )
    ''')
    
    # Clients table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            address TEXT
        )
    ''')
    
    # Invoices table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_number TEXT NOT NULL,
            client_id INTEGER,
            date TEXT NOT NULL,
            total_amount REAL,
            status TEXT DEFAULT 'unpaid',
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')
    
    # Invoice items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_id INTEGER,
            description TEXT,
            quantity INTEGER,
            unit_price REAL,
            total REAL,
            FOREIGN KEY (invoice_id) REFERENCES invoices(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Database initialized")


def execute_query(query: str, params: tuple = (), fetch: bool = False):
    """Execute a query and optionally fetch results"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    if fetch:
        result = cursor.fetchall()
        conn.close()
        return result
    
    conn.commit()
    conn.close()


def execute_many(query: str, params_list: list):
    """Execute multiple queries"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executemany(query, params_list)
    conn.commit()
    conn.close()
