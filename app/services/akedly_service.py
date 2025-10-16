# backend/akedly_service.py
import requests
import os
from app.config import AKEDLY_API_KEY, PIPELINE_ID, BASE_URL


AKEDLY_API_KEY = os.getenv("AKEDLY_API_KEY") 
PIPELINE_ID = os.getenv("AKEDLY_PIPELINE_ID") 
BASE_URL = os.getenv("BASE_URL")


def create_transaction(phone_number: str):
    """
    Step 1: Create a new OTP transaction for the provided phone number.
    Returns the transaction ID.
    """
    payload = {
        "APIKey": AKEDLY_API_KEY,
        "pipelineID": PIPELINE_ID,
        "verificationAddress": {
            "phoneNumber": phone_number
        },
        "digits": 6
    }

    response = requests.post(BASE_URL, json=payload)
    data = response.json()

    if response.status_code == 200 and "transactionId" in data:
        return {"success": True, "transactionId": data["transactionId"]}
    else:
        return {"success": False, "error": data}


def activate_transaction(transaction_id: str):
    """
    Step 2: Activate the OTP transaction.
    """
    url = f"{BASE_URL}/activate/{transaction_id}"
    response = requests.post(url, json={})
    if response.status_code == 200:
        return {"success": True}
    else:
        return {"success": False, "error": response.json()}


def verify_otp(transaction_id: str, otp: str):
    """
    Step 3: Verify the OTP entered by the user.
    """
    url = f"{BASE_URL}/verify/{transaction_id}"
    payload = {"otp": otp}
    response = requests.post(url, json=payload)
    data = response.json()

    if response.status_code == 200 and data.get("verified") is True:
        return {"verified": True, "data": data}
    else:
        return {"verified": False, "data": data}
