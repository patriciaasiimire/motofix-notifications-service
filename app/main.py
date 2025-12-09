# app/main.py
from fastapi import FastAPI
from .routers import notifications

app = FastAPI(
    title="MOTOFIX Notifications Service",
    description="SMS + WhatsApp alerts for mechanics and customers",
    version="1.0.0"
)

app.include_router(notifications.router)