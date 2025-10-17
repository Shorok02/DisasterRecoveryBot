# ...existing code...
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import logging
from app.services.akedly_service import create_transaction, activate_transaction, verify_transaction
from app.core.session_manager import SessionManager

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="DR Bot Backend (Akedly adapter)")
session_mgr = SessionManager()

class SendOtpReq(BaseModel):
    phone: str

class VerifyOtpReq(BaseModel):
    # note: verify expects internal_id (from activate) in the url, but we'll accept as field name "internal_id"
    internal_id: str
    otp: str
    phone: str = None  # optional; we store session by phone


@app.get("/")
def health_check():
    return {"status": "ok", "message": "FastAPI is live"}


@app.post("/api/send-otp")
async def send_otp(req: SendOtpReq):
    logging.info("send-otp called for phone=%s", req.phone)
    try:
        # 1) create transaction -> get public transactionID
        create_result = await create_transaction(req.phone)
        if not create_result.get("success"):
            logging.warning("create_transaction failed: %s", create_result.get("raw"))
            raise HTTPException(status_code=502, detail="Failed to create transaction")

        transaction_id = create_result.get("transactionID")
        if not transaction_id:
            logging.warning("create_transaction returned no transactionID: %s", create_result.get("raw"))
            # still return raw for debugging
            return {"status": "error", "data": create_result.get("raw"), "message": "transactionID missing from create response"}

        # 2) activate using transactionID -> activation returns internal _id
        activate_result = await activate_transaction(transaction_id)
        if not activate_result.get("success"):
            logging.warning("activate_transaction failed for %s: %s", transaction_id, activate_result.get("raw"))
            # return what we have for debugging
            return {"status": "error", "data": activate_result.get("raw"), "message": "Failed to activate transaction"}

        internal_id = activate_result.get("internal_id")
        if not internal_id:
            logging.warning("activate_transaction missing internal_id, raw=%s", activate_result.get("raw"))
            # return success with raw but indicate missing internal id
            return {
                "status": "success",
                "data": {"transactionID": transaction_id, "internal_id": internal_id},
                "message": "Main transaction created but internal_id missing; check activate response",
                "raw_activate": activate_result.get("raw")
            }

        # 3) success: return both IDs to the caller (bot)
        return {
            "status": "success",
            "data": {"transactionID": transaction_id, "internal_id": internal_id},
            "message": "Main transaction created successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.exception("send-otp error")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/verify-otp")
async def verify_otp(req: VerifyOtpReq):
    logging.info("verify-otp called internal_id=%s phone=%s", req.internal_id, req.phone)
    try:
        result = await verify_transaction(req.internal_id, req.otp)
        if result.get("verified"):
            if req.phone:
                session_mgr.create_session(req.phone)
            return {"verified": True}
        return {"verified": False, "data": result.get("data")}
    except Exception as e:
        logging.exception("verify-otp error")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/otp-callback")
async def otp_callback(request: Request):
    logging.info("OTP callback arrived")
    body = await request.json()
    logging.info("Received Akedly callback: %s", body)
    return {"received": True}
# ...existing code...