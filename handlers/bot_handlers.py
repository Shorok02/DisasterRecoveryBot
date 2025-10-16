# handlers/bot_handlers.py

from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from config import SESSION_DURATION_HOURS
from services.email_service import send_otp_email
from utils.session_utils import is_session_active
from db.database import get_otp, delete_otp, save_user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Some DR Bot.\nPlease enter your registered email address:")
    context.user_data["state"] = "AWAITING_EMAIL"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    state = context.user_data.get("state")

    if state == "AWAITING_EMAIL":
        email = text
        success = send_otp_email(email)
        if success:
            await update.message.reply_text(f"📩 OTP sent to {email}. Please enter it below:")
            context.user_data["state"] = "AWAITING_OTP"
            context.user_data["email"] = email
        else:
            await update.message.reply_text("⚠️ Failed to send OTP. Try again later.")

    elif state == "AWAITING_OTP":
        email = context.user_data.get("email")
        otp_data = get_otp(email)

        if not otp_data:
            await update.message.reply_text("⚠️ No OTP found. Please restart with /start.")
            return

        otp, expiry = otp_data
        if datetime.now() > datetime.fromisoformat(expiry):
            await update.message.reply_text("❌ OTP expired. Please /start again.")
            delete_otp(email)
            return

        if text == otp:
            expiry_time = datetime.now() + timedelta(hours=SESSION_DURATION_HOURS)
            save_user(email, user_id, expiry_time)
            delete_otp(email)
            context.user_data["state"] = "LOGGED_IN"

            await update.message.reply_text(
                "✅ Verified! Session active for 1 hour.\nChoose an option:",
                reply_markup=ReplyKeyboardMarkup(
                    [["💰 Balance", "📊 Positions", "🧾 Accounts"]], resize_keyboard=True
                )
            )
        else:
            await update.message.reply_text("❌ Invalid OTP. Try again.")

    elif text in ["💰 Balance", "📊 Positions", "🧾 Accounts"]:
        if not is_session_active(user_id):
            await update.message.reply_text("⚠️ Session expired. Please verify again with /start.")
            return

        if text == "💰 Balance":
            await update.message.reply_text("💰 Your balance is $5,430.")
        elif text == "📊 Positions":
            await update.message.reply_text("📊 2 open positions:\n- Gold/USD: +1.2%\n- Oil/USD: -0.3%")
        elif text == "🧾 Accounts":
            await update.message.reply_text("🧾 Linked accounts:\n- Main Wallet\n- Demo Wallet")
