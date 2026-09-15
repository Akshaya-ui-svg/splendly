import sqlite3
import os
from flask import g, current_app
from werkzeug.security import generate_password_hash
from datetime import datetime

DATABASE = 'spendly.db'

def get_db_connection(path=None):
    """
    Utility to get a raw SQLite connection.
    Ensures foreign keys are enabled and rows are returned as Row objects.
    """
    if path is None:
        try:
            # Use app root path if within a Flask request context
            path = os.path.join(current_app.root_path, DATABASE)
        except RuntimeError:
            # Fallback to current working directory if not in context
            path = DATABASE

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def get_db():
    """
    Returns the database connection for the current request.
    The connection is stored in the Flask 'g' object and persists for the request.
    """
    if 'db' not in g:
        g.db = get_db_connection()
    return g.db

def create_user(name, email, password_hash):
    """
    Creates a new user in the database.
    Returns the new user's ID on success.
    Raises sqlite3.IntegrityError if the email already exists.
    """
    db = get_db()
    cursor = db.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        (name, email, password_hash)
    )
    db.commit()
    return cursor.lastrowid

def init_db():
    """
    Initializes the database by creating the users and expenses tables.
    """
    with get_db_connection() as conn:
        # Users table: stores authentication and profile info
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        ''')

        # Expenses table: stores individual expense records
        conn.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL CHECK (category IN ('Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Shopping', 'Other')),
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        conn.commit()

def seed_db():
    """
    Seeds the database with sample users and expenses for development.
    """
    with get_db_connection() as conn:
        # Seed demo user
        demo_email = 'demo@spendly.com'
        user = conn.execute('SELECT id FROM users WHERE email = ?', (demo_email,)).fetchone()

        if not user:
            hashed_pw = generate_password_hash('demo123')
            conn.execute(
                'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
                ('Demo User', demo_email, hashed_pw)
            )
            conn.commit()

        # Get the user ID for seeding expenses
        user_row = conn.execute('SELECT id FROM users WHERE email = ?', (demo_email,)).fetchone()
        user_id = user_row['id']

        # Seed 8 expenses for the current month across all categories
        current_date = datetime.now().strftime('%Y-%m-%d')

        categories = ['Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Shopping', 'Other']
        expenses = [
            (user_id, 15.50, 'Food', current_date, 'Lunch at cafe'),
            (user_id, 45.00, 'Transport', current_date, 'Gas fill-up'),
            (user_id, 120.00, 'Bills', current_date, 'Electric bill'),
            (user_id, 30.00, 'Health', current_date, 'Pharmacy'),
            (user_id, 60.00, 'Entertainment', current_date, 'Movie night'),
            (user_id, 85.00, 'Shopping', current_date, 'New shoes'),
            (user_id, 10.00, 'Other', current_date, 'Misc items'),
            (user_id, 20.00, 'Food', current_date, 'Dinner delivery'),
        ]

        # Prevent duplicate inserts on repeated runs
        existing_count = conn.execute('SELECT COUNT(*) as count FROM expenses WHERE user_id = ?', (user_id,)).fetchone()['count']
        if existing_count == 0:
            conn.executemany(
                'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
                expenses
            )
            conn.commit()
