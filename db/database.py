# db/database.py

import sqlite3
from datetime import datetime
from config import DB_NAME


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            telegram_id INTEGER,
            session_expiry DATETIME
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS otps (
            email TEXT PRIMARY KEY,
            otp TEXT,
            expiry DATETIME
        )
    """)
    conn.commit()
    conn.close()


# ==========================
# OTP Handling
# ==========================
def save_otp(email, otp, expiry):
    conn = get_connection()
    c = conn.cursor()
    c.execute("REPLACE INTO otps (email, otp, expiry) VALUES (?, ?, ?)", (email, otp, expiry))
    conn.commit()
    conn.close()


def get_otp(email):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT otp, expiry FROM otps WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    return row


def delete_otp(email):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM otps WHERE email=?", (email,))
    conn.commit()
    conn.close()


# ==========================
# User Handling
# ==========================
def save_user(email, telegram_id, session_expiry):
    conn = get_connection()
    c = conn.cursor()
    c.execute("REPLACE INTO users (email, telegram_id, session_expiry) VALUES (?, ?, ?)",
              (email, telegram_id, session_expiry))
    conn.commit()
    conn.close()


def get_user_by_telegram_id(telegram_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT session_expiry FROM users WHERE telegram_id=?", (telegram_id,))
    row = c.fetchone()
    conn.close()
    return row
