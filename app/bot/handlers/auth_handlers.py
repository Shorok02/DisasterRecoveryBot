import httpx
from telegram import Update
from telegram.ext import ContextTypes
import logging


BACKEND_URL = "http://localhost:8000/api"  # replace with your backend URL
print("auth_handlers.py imported")

async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    context.user_data["phone"] = phone

    try:
        print(f"Calling backend /send-otp for phone: {phone}")
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{BACKEND_URL}/send-otp", json={"phone": phone})
            result = resp.json()
            print(f"/send-otp result: {result}")


        # Corrected parsing based on your actual backend response
        if result.get("success"):
            txn = result.get("transactionId")
            context.user_data["transaction_id"] = txn
            logging.info(f"Stored transaction ID: {txn}")
            await update.message.reply_text(f"OTP sent to {phone}. Please enter the code.")
        else:
            await update.message.reply_text(f"Failed to send OTP. Response: {result.get('message') or result}")

    except Exception as e:
        await update.message.reply_text(f"Error sending OTP: {e}")


# ------------------- Handle OTP -------------------
async def handle_otp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    otp = update.message.text.strip()
    phone = context.user_data.get("phone")
    txn_id = context.user_data.get("transaction_id")

    if not txn_id:
        await update.message.reply_text("No transaction found. Please start by sending your phone number.")
        return

    try:
        print(f"Verifying OTP {otp} for transaction {txn_id}")
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BACKEND_URL}/verify-otp",
                json={"transactionId": txn_id, "otp": otp, "phone": phone}
            )
            result = resp.json()

        print(f"/verify-otp result: {result}")

        if result.get("verified"):
            await update.message.reply_text("OTP verified successfully! ✅")
            # Optionally clear session
            context.user_data.clear()
        else:
            await update.message.reply_text(f"OTP verification failed. Response: {result.get('data') or result}")

    except Exception as e:
        await update.message.reply_text(f"Error verifying OTP: {e}")
