# app/bot/handlers/auth_handlers.py
import requests
from app.config import BACKEND_BASE_URL
from telegram import Update
from telegram.ext import ContextTypes

BACKEND_SEND = f"{BACKEND_BASE_URL}/send-otp"
BACKEND_VERIFY = f"{BACKEND_BASE_URL}/verify-otp"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Amana DR. Please send your phone number (e.g. +2010xxxx).")

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    context.user_data["phone"] = phone
    try:
        res = requests.post(BACKEND_SEND, json={"phone": phone}, timeout=10)
        if res.status_code == 200 and res.json().get("success"):
            txn = res.json().get("transactionId")
            context.user_data["transaction_id"] = txn
            await update.message.reply_text(f"OTP sent to {phone}. Please enter the code.")
        else:
            await update.message.reply_text(f"Failed to send OTP. Response: {res.text}")
    except Exception as e:
        await update.message.reply_text(f"Error sending OTP: {e}")

async def handle_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    otp = update.message.text.strip()
    txn = context.user_data.get("transaction_id")
    phone = context.user_data.get("phone")
    if not txn:
        await update.message.reply_text("No active transaction. Please send your phone number again with /start.")
        return
    try:
        res = requests.post(BACKEND_VERIFY, json={"transactionId": txn, "otp": otp, "phone": phone}, timeout=10)
        if res.status_code == 200 and res.json().get("verified"):
            await update.message.reply_text("✅ OTP verified — you are authenticated for 1 hour. Type /menu")
            context.user_data["authenticated"] = True
        else:
            await update.message.reply_text("❌ Invalid OTP or verification failed.")
    except Exception as e:
        await update.message.reply_text(f"Error verifying OTP: {e}")
