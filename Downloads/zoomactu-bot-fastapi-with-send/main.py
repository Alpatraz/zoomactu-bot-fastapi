from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_USER_ID = os.getenv("TELEGRAM_USER_ID")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.get("/")
def read_root():
    return {"status": "ZoomActuBot is live!"}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    message = data.get("message", {}).get("text", "")
    chat_id = data.get("message", {}).get("chat", {}).get("id", "")

    if message.lower() == "/start":
        requests.post(TELEGRAM_API_URL, data={"chat_id": chat_id, "text": "🤖 ZoomActuBot est connecté et actif !"})
    return {"ok": True}


@app.get("/send")
def send_message(msg: str = "Test ZoomActu"):
    if not TELEGRAM_TOKEN or not TELEGRAM_USER_ID:
        return {"error": "Missing Telegram configuration"}
    response = requests.post(TELEGRAM_API_URL, data={
        "chat_id": TELEGRAM_USER_ID,
        "text": msg
    })
    return {"status": "Message sent", "response": response.json()}
