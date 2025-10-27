import sqlite3

conn = sqlite3.connect("bot_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    phone_number TEXT PRIMARY KEY,
    balance REAL DEFAULT 0,
    positions TEXT,
)
""")

conn.commit()
conn.close()
