import sqlite3
import os
import sys
from werkzeug.security import check_password_hash
from database.db import DATABASE, init_db, seed_db

def verify_database():
    # 1. Setup: Initialize and Seed
    print("Initializing and seeding database for verification...")
    init_db()
    seed_db()

    db_path = DATABASE
    if not os.path.exists(db_path):
        print(f"Error: Database file {db_path} not found.")
        return False

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    try:
        print("\n--- Verifying Schema ---")
        # Verify users table
        user_table = cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users'").fetchone()
        if not user_table:
            print("Error: users table missing")
            return False
        print("Users table exists.")

        # Verify expenses table
        expense_table = cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='expenses'").fetchone()
        if not expense_table:
            print("Error: expenses table missing")
            return False
        print("Expenses table exists.")

        print("\n--- Verifying Constraints ---")
        # Verify Foreign Key constraint
        try:
            cursor.execute("INSERT INTO expenses (user_id, amount, category, date) VALUES (9999, 10.0, 'Food', '2023-01-01')")
            print("Error: Foreign key constraint NOT enforced (inserted expense for non-existent user)")
            return False
        except sqlite3.IntegrityError:
            print("Foreign key constraint enforced.")

        # Verify Category constraint
        try:
            # Get a valid user first
            user = cursor.execute("SELECT id FROM users LIMIT 1").fetchone()
            if not user:
                print("Error: No users found to test category constraint")
                return False
            cursor.execute("INSERT INTO expenses (user_id, amount, category, date) VALUES (?, 10.0, 'Luxury', '2023-01-01')", (user['id'],))
            print("Error: Category constraint NOT enforced (inserted invalid category 'Luxury')")
            return False
        except sqlite3.IntegrityError:
            print("Category constraint enforced.")

        print("\n--- Verifying Seed Data ---")
        # Verify Demo User
        user = cursor.execute("SELECT * FROM users WHERE email = 'demo@spendly.com'").fetchone()
        if not user:
            print("Error: Demo user missing")
            return False

        if not check_password_hash(user['password_hash'], 'demo123'):
            print("Error: Demo user password hash is incorrect")
            return False
        print("Demo user verified with correct password hash.")

        # Verify Expenses
        expenses = cursor.execute("SELECT * FROM expenses WHERE user_id = ?", (user['id'],)).fetchall()
        if len(expenses) != 8:
            print(f"Error: Expected 8 expenses, found {len(expenses)}")
            return False

        categories_found = {exp['category'] for exp in expenses}
        required_categories = {'Food', 'Transport', 'Bills', 'Health', 'Entertainment', 'Shopping', 'Other'}
        if not required_categories.issubset(categories_found):
            print(f"Error: Missing categories. Found: {categories_found}")
            return False
        print("Seed expenses verified (8 records, all categories present).")

        print("\n--- All database tests passed! ---")
        return True

    except Exception as e:
        print(f"Unexpected error during verification: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    if verify_database():
        sys.exit(0)
    else:
        sys.exit(1)
