from fastapi import APIRouter, HTTPException
import os
import logging

router = APIRouter(prefix="/notify", tags=["Notifications"])

# Try to import Africa's Talking — fall back gracefully
try:
    import africastalking
    AT_USERNAME = os.getenv("AT_USERNAME", "sandbox")
    AT_API_KEY = os.getenv("AT_API_KEY")
    africastalking.initialize(AT_USERNAME, AT_API_KEY)
    sms = africastalking.SMS
    whatsapp = africastalking.WhatsApp
    AT_READY = True
except Exception as e:
    logging.warning(f"Africa's Talking not available: {e}")
    AT_READY = False

@router.post("/sms")
async def send_sms(to: str, message: str):
    if not AT_READY:
        return {"status": "fake", "to": to, "message": message, "note": "AT not configured"}
    
    try:
        response = sms.send(message, [to])
        return {"status": "sent", "provider": "SMS", "response": response}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@router.post("/whatsapp")
async def send_whatsapp(to: str, message: str):
    if not AT_READY:
        return {"status": "fake", "to": to, "message": message, "note": "WhatsApp test mode"}
    
    try:
        response = whatsapp.send(message=message, recipients=[to])
        return {"status": "sent", "provider": "WhatsApp", "response": response}
    except Exception as e:
        raise HTTPException(500, detail=str(e))