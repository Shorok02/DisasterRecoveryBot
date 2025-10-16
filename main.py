# main.py

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from handlers.bot_handlers import start, handle_message
from db.database import init_db
from config import BOT_TOKEN


def main():
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Amana DR Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
