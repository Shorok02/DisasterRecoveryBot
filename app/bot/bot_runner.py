# app/bot/bot_runner.py
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from app.config import TELEGRAM_BOT_TOKEN
from app.bot.handlers import auth_handlers, bot_handlers, fallback_handler

def start_bot():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # auth flow
    #TODO: Pitfall, improve phone regex and otp, for now swapped them so otp does not fall into phone regex
    app.add_handler(CommandHandler("start", auth_handlers.start))
    app.add_handler(MessageHandler(filters.Regex(r"^\d{3,6}$"), auth_handlers.handle_otp))

    app.add_handler(MessageHandler(filters.Regex(r"^\+?\d+$"), auth_handlers.handle_phone))

    # menu / features
    app.add_handler(CommandHandler("menu", bot_handlers.show_menu))
    app.add_handler(MessageHandler(filters.Regex(r"^Check Balance$"), bot_handlers.handle_balance))
    app.add_handler(MessageHandler(filters.Regex(r"^Open Positions$"), bot_handlers.handle_positions))
    app.add_handler(MessageHandler(filters.Regex(r"^Logout$"), bot_handlers.handle_logout))

    # fallback
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fallback_handler.fallback))

    print("🤖 Telegram bot started (polling)...")
    app.run_polling()
