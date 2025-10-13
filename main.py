from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

#from botfather --> is that okay?
BOT_TOKEN = "8262843336:AAFzoxIF9CaEQ3iz06ujRKsZLwfv7yQdJ14"

# --- Define the menus ---
# TODO: separate menus into different files to accommodate more complex logic
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("💰 Balance", callback_data="balance")],
        [InlineKeyboardButton("📈 Positions", callback_data="positions")],
        [InlineKeyboardButton("🔗 Linked Accounts", callback_data="accounts")]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("⬅️ Back to Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)


# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to Test Disaster Recovery Bot!\nChoose an option below:",
        reply_markup=main_menu_keyboard()
    )


# --- Callback Handlers ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "balance":
        await query.message.reply_text(
            text="💰 *Your Balance:*\n\n- USD: 2,500.00\n- AED: 9,180.00",
            parse_mode="Markdown",
            reply_markup=back_to_main_menu_keyboard()
        )

    elif query.data == "positions":
        await query.message.reply_text(
            text="📈 *Open Positions:*\n\n- GOLD/USD: +2.4%\n- BTC/USD: -1.2%",
            parse_mode="Markdown",
            reply_markup=back_to_main_menu_keyboard()
        )

    elif query.data == "accounts":
        await query.message.reply_text(
            text="🔗 *Linked Accounts:*\n\n- Account #12345\n- Account #67890",
            parse_mode="Markdown",
            reply_markup=back_to_main_menu_keyboard()
        )

    elif query.data == "main_menu":
        await query.message.reply_text(
            text="🏠 Main Menu — choose an option:",
            reply_markup=main_menu_keyboard()
        )

# --- Run the bot ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("✅ Bot is running... press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
