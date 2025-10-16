# app/bot/handlers/bot_handlers.py
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

MENU = [["💰 Check Balance", "📊 Open Positions"], ["🚪 Logout"]]

async def show_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("authenticated"):
        await update.message.reply_text("Please authenticate first with /start.")
        return
    await update.message.reply_text("Main menu:", reply_markup=ReplyKeyboardMarkup(MENU, resize_keyboard=True))

async def handle_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("authenticated"):
        await update.message.reply_text("Please authenticate first with /start.")
        return
    # demo data
    await update.message.reply_text("💰 Balance: USD 12,340.50")

async def handle_positions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("authenticated"):
        await update.message.reply_text("Please authenticate first with /start.")
        return
    await update.message.reply_text("📊 Positions:\n1. GOLD/USD: +1.2%\n2. BTC/USD: -0.8%")

async def handle_logout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("Logged out. Use /start to authenticate again.")
