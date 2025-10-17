# app/backend/app.py
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from app.services.akedly_service import create_transaction, activate_transaction, verify_transaction
from app.core.session_manager import SessionManager

app = FastAPI(title="DR Bot Backend (Akedly adapter)")
session_mgr = SessionManager()

class SendOtpReq(BaseModel):
    phone: str

class VerifyOtpReq(BaseModel):
    transactionId: str
    otp: str
    phone: str = None  # optional; we store session by phone


@app.get("/")
def health_check():
    return {"status": "ok", "message": "FastAPI is live"}


@app.post("/api/send-otp")
async def send_otp(req: SendOtpReq):
    print ("hello send otp")
    try:
        print('helloooooo')
        data = await create_transaction(req.phone)
        # transactionId location depends on Akedly response structure.
        # adapt to actual key name; docs sample implied transactionId present in response.
        transaction_id = data.get("transactionID", None)
        if not transaction_id:
            # return whole payload for debugging
            print("transactionId: "+ transaction_id)
            return {"success": False, "raw": data}
        # activate it
        await activate_transaction(transaction_id)
        return {"success": True, "transactionId": transaction_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/api/verify-otp")
async def verify_otp(req: VerifyOtpReq):
    try:
        data = await verify_transaction(req.transactionId, req.otp)
        # Akedly responses may vary. Assume a "verified" flag or status field.
        # Example: data.get("status") == "verified" or data.get("verified") == True
        verified = False
        if isinstance(data, dict):
            if data.get("verified") is True:
                verified = True
            elif data.get("status") == "verified":
                verified = True
        if verified:
            if req.phone:
                session_mgr.create_session(req.phone)
            return {"verified": True}
        return {"verified": False, "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/otp-callback")
async def otp_callback(request: Request):
    print("I just arrived")
    body = await request.json()
    # For now just log and acknowledge; you can update sessions or logs here.
    print("Received Akedly callback:", body)
    return {"received": True}
