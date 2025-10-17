# ...existing code...
import httpx
import os
import logging
from app.config import AKEDLY_API_KEY as CFG_AK, PIPELINE_ID as CFG_PIPELINE, AKEDLY_BASE_URL as CFG_BASE

logging.basicConfig(level=logging.INFO)

AKEDLY_API_KEY = os.getenv("AKEDLY_API_KEY", CFG_AK)
PIPELINE_ID = os.getenv("AKEDLY_PIPELINE_ID", CFG_PIPELINE)
AKEDLY_BASE_URL = os.getenv("AKEDLY_BASE_URL", CFG_BASE)


async def create_transaction(phone_number: str):
    logging.info("Creating transaction for phone number: %s", phone_number)
    payload = {
        "APIKey": AKEDLY_API_KEY,
        "pipelineID": PIPELINE_ID,
        "verificationAddress": {"phoneNumber": phone_number},
        "digits": 6,
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(AKEDLY_BASE_URL, json=payload, timeout=15)
        data = resp.json()

    logging.info("create_transaction response status=%s body=%s", resp.status_code, data)

    # Expect Akedly create response shape: {"status":"success","data":{"transactionID": "..."} ...}
    if resp.status_code == 200 and isinstance(data, dict) and data.get("data"):
        txn_data = data["data"]
        transaction_id = (
            txn_data.get("transactionID")
            or txn_data.get("transactionId")
            or txn_data.get("mainTransactionID")
            or txn_data.get("mainTransactionId")
            or txn_data.get("id")
        )
        # We don't expect internal_id from create; return what we have and raw for debugging
        return {
            "success": True,
            "transactionID": transaction_id,
            "raw": data
        }

    return {"success": False, "raw": data, "status_code": resp.status_code}


async def activate_transaction(transaction_id: str):
    """Activate OTP using public transactionID. Activation response contains internal _id."""
    url = f"{AKEDLY_BASE_URL}/activate/{transaction_id}"
    logging.info("Activating transaction %s -> %s", transaction_id, url)
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json={}, timeout=15)
        data = resp.json()

    logging.info("activate_transaction response status=%s body=%s", resp.status_code, data)

    if resp.status_code == 200 and isinstance(data, dict):
        # activation response contains data._id per your example
        internal_id = None
        if data.get("data") and isinstance(data["data"], dict):
            internal_id = data["data"].get("_id") or data["data"].get("internal_id") or data["data"].get("id")
        return {"success": True, "internal_id": internal_id, "raw": data}

    return {"success": False, "raw": data, "status_code": resp.status_code}


async def verify_transaction(internal_id: str, otp: str):
    """Verify OTP using internal _id (from activate response)."""
    url = f"{AKEDLY_BASE_URL}/verify/{internal_id}"
    payload = {"otp": otp}
    logging.info("Verifying transaction %s with otp", internal_id)
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, timeout=15)
        data = resp.json()

    logging.info("verify_transaction response status=%s body=%s", resp.status_code, data)

    if resp.status_code == 200 and isinstance(data, dict):
        # verified = False
        # if data.get("status") == "verified" or data.get("verified") is True:
        #     verified = True
        # # some providers embed verification in data
        # if data.get("data") and isinstance(data["data"], dict):
        #     if data["data"].get("status") == "verified" or data["data"].get("verified") is True:
        #         verified = True
        return {"verified": True, "data": data}

    return {"verified": False, "data": data, "status_code": resp.status_code}
# ...existing code...