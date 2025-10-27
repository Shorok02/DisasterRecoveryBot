import sqlite3
import json

DB_PATH = "bot_data.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)


def initialize_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        phone_number TEXT PRIMARY KEY,
        balance REAL DEFAULT 0,
        positions TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_user(phone_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (phone_number) VALUES (?)", (phone_number,))
    conn.commit()
    conn.close()
    
def get_user(phone_number):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT phone_number, balance, positions FROM users WHERE phone_number = ?", (phone_number,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "phone_number": row[0],
            "balance": row[1],
            "positions": json.loads(row[2]) if row[2] else []
        }
    return None