# ...existing code...
import httpx
import logging
from telegram import Update
from telegram.ext import ContextTypes
from app.bot.handlers import bot_handlers
import asyncio


logging.basicConfig(level=logging.INFO)
BACKEND_HOST = "http://localhost:8000"
SEND_OTP_PATH = "/api/send-otp"
VERIFY_OTP_PATH = "/api/verify-otp"
logging.info("auth_handlers.py imported")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Received /start command from user %s", update.effective_user.id if update.effective_user else "unknown")
    await update.message.reply_text(
        "Welcome to Amana DR. Please send your phone number (e.g. +2010xxxx) to receive an OTP."
    )

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    context.user_data["phone"] = phone

    try:
        url = f"{BACKEND_HOST}{SEND_OTP_PATH}"
        logging.info("Calling backend %s for phone: %s", url, phone)
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json={"phone": phone}, timeout=15)
            result = resp.json()
        logging.info("POST %s -> status=%s body=%s", url, resp.status_code, result)

        # Expecting: {"status":"success","data":{"transactionID": "...", "internal_id": "..."},"message": ...}
        if result.get("status") == "success" and isinstance(result.get("data"), dict):
            data = result["data"]
            txn = data.get("transactionID")
            internal_id = data.get("internal_id")
            context.user_data["transaction_id"] = txn
            context.user_data["internal_id"] = internal_id
            logging.info("Stored transactionID=%s internal_id=%s for user", txn, internal_id)
            await update.message.reply_text(f"OTP sent to {phone}. Please enter the code.")
        else:
            await update.message.reply_text(f"Failed to send OTP. Response: {result.get('message') or result}")

    except Exception as e:
        logging.exception("handle_phone error")
        await update.message.reply_text(f"Error sending OTP: {e}")


async def handle_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    otp = update.message.text.strip()
    phone = context.user_data.get("phone")
    internal_id = context.user_data.get("internal_id")

    if not internal_id:
        await update.message.reply_text("No transaction found (internal_id). Please start by sending your phone number.")
        return

    try:
        url = f"{BACKEND_HOST}{VERIFY_OTP_PATH}"
        logging.info("Calling backend %s to verify internal_id=%s otp=%s", url, internal_id, otp)
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json={"internal_id": internal_id, "otp": otp, "phone": phone}, timeout=15)
            result = resp.json()
        logging.info("POST %s -> status=%s body=%s", url, resp.status_code, result)

        if result.get("verified"):
            await update.message.reply_text("OTP verified successfully! ✅")
            logging.info("User verified, preparing to show menu for phone=%s", phone)
            context.user_data["authenticated"] = True

            # call show_menu whether it's async or sync
            menu_callable = bot_handlers.show_menu
            try:
                if asyncio.iscoroutinefunction(menu_callable):
                    await menu_callable(update, context)
                else:
                    # run sync handler in executor to avoid blocking event loop
                    await asyncio.get_event_loop().run_in_executor(None, menu_callable, update, context)
                logging.info("show_menu completed successfully")
            except Exception:
                logging.exception("show_menu failed")
            context.user_data.clear()
        else:
            await update.message.reply_text(f"OTP verification failed. Response: {result.get('data') or result}")

    except Exception as e:
        logging.exception("handle_otp error")
        await update.message.reply_text(f"Error verifying OTP: {e}")

