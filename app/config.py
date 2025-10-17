# config.py

# BOT_TOKEN = "8262843336:AAFzoxIF9CaEQ3iz06ujRKsZLwfv7yQdJ14"

# # Email credentials
# EMAIL_SENDER = "shorokabdulraof@gmail.com"
# EMAIL_PASSWORD = "jpcrobgsfnoqguzt"
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587

# # Session duration
# SESSION_DURATION_HOURS = 1
# OTP_EXPIRY_MINUTES = 5

# # Database name
# DB_NAME = "amana.db"


import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram Bot
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Akedly OTP API configuration
AKEDLY_API_KEY = os.getenv("AKEDLY_API_KEY") 
PIPELINE_ID = os.getenv("AKEDLY_PIPELINE_ID") 
AKEDLY_BASE_URL = "https://api.akedly.io/api/v1/transactions"

# General settings
OTP_EXPIRY_MINUTES = 5
SESSION_DURATION_HOURS = 1



