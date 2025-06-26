
import os
from fastapi import FastAPI, Request
import requests

app = FastAPI()

TOKEN = os.getenv("TELEGRAM_TOKEN")
SMM_API_KEY = os.getenv("SMM_KEY")
SMM_API_URL = os.getenv("API_URL")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": chat_id, "text": text})

def send_photo(chat_id, photo_url, caption=""):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"
    requests.post(url, json={"chat_id": chat_id, "photo": photo_url, "caption": caption})

@app.post("/webhook/{token}")
async def webhook(token: str, request: Request):
    if token != TOKEN:
        return {"status": "unauthorized"}
    data = await request.json()
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").lower()
    photo = message.get("photo", None)

    if text == "/start":
        send_message(chat_id, "👋 Welcome to Rise Online Bot!
Select a platform:
1. Instagram
2. YouTube")
    elif "instagram" in text:
        send_message(chat_id, "Choose a service:
1. Followers
2. Likes
3. Views
4. Comments
5. Engagement")
    elif "youtube" in text:
        send_message(chat_id, "Choose a service:
1. Views
2. Subscribers
3. Likes
4. Comments")
    elif text.isdigit():
        quantity = int(text)
        price = quantity * 0.18
        send_photo(chat_id, "https://chat.openai.com/cdn/qr-riseonline.png",
                   caption=f"💰 Total: ₹{price:.2f}
📲 Pay to UPI: 8188938018@fam
Or scan the QR code above.

📸 After payment, send the payment *screenshot* here.")
    elif photo:
        file_id = photo[-1].get("file_id")
        send_message(chat_id, "🕐 Please wait while we verify your payment screenshot.")
        send_message(ADMIN_CHAT_ID, f"📥 New payment screenshot received from user {chat_id}.
Approve this payment?
Reply /approve_{chat_id} or /reject_{chat_id}")
    elif text.startswith("/approve_"):
        user_id = text.split("_")[1]
        send_message(user_id, "✅ Payment approved! Your order has been placed.")
    elif text.startswith("/reject_"):
        user_id = text.split("_")[1]
        send_message(user_id, "❌ Payment failed. Please check your screenshot or contact @riseonlineofficial.")
    else:
        send_message(chat_id, "Send /start to begin.")

    return {"ok": True}
