# app/bot/handlers/fallback_handler.py
from telegram import Update
from telegram.ext import ContextTypes

async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sorry, I didn't understand. Use /menu to see options.")
