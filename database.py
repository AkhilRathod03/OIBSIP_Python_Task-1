
import sqlite3
import os
from datetime import datetime

# Get the absolute path of the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the path to the database file, ensuring it's in the same directory
DB_FILE = os.path.join(BASE_DIR, "bmi_data.db")

def initialize_database():
    """Initializes the database and creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bmi_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            weight REAL NOT NULL,
            height REAL NOT NULL,
            bmi REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_bmi_record(name, age, weight, height, bmi, category):
    """Saves a new BMI record to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("""
            INSERT INTO bmi_records (name, age, weight, height, bmi, category, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, age, weight, height, bmi, category, date_str))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

def get_user_history(name):
    """Retrieves all BMI records for a specific user (case-insensitive)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT date, bmi, category, weight, height, age FROM bmi_records WHERE UPPER(name) = UPPER(?) ORDER BY date ASC", (name,))
    records = cursor.fetchall()
    conn.close()
    return records

# Initialize the database on first import
initialize_database()
