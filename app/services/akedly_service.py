
import requests
import os
from app.config import AKEDLY_API_KEY, PIPELINE_ID, AKEDLY_BASE_URL


AKEDLY_API_KEY = os.getenv("AKEDLY_API_KEY") 
PIPELINE_ID = os.getenv("AKEDLY_PIPELINE_ID") 


def create_transaction(phone_number: str):
    print(f"Creating transaction for phone number: {phone_number}")
    payload = {
        "APIKey": AKEDLY_API_KEY,
        "pipelineID": PIPELINE_ID,
        "verificationAddress": {
            "phoneNumber": phone_number
        },
        "digits": 6
    }

    response = requests.post(AKEDLY_BASE_URL, json=payload)
    data = response.json()
    
    if response.status_code == 200 and "transactionID" in data["data"]:
        return {"success": True, "transactionID": data["data"]["transactionID"]}
    else:
        return {"success": False, "error": data}

def activate_transaction(transaction_id: str):
    url = f"{AKEDLY_BASE_URL}/activate/{transaction_id}"
    response = requests.post(url, json={})
    if response.status_code == 200:
        return {"success": True}
    else:
        return {"success": False, "error": response.json()}

def verify_transaction(transaction_id: str, otp: str):
    url = f"{AKEDLY_BASE_URL}/verify/{transaction_id}"
    payload = {"otp": otp}
    response = requests.post(url, json=payload)
    data = response.json()

    if response.status_code == 200 and data.get("verified") is True:
        return {"verified": True, "data": data}
    else:
        return {"verified": False, "data": data}