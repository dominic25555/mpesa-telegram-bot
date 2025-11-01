# mpesa-telegram-bot
A Telegram bot that accepts M-Pesa payments via Daraja API
import requests
import base64
from datetime import datetime
from telegram.ext import Application, CommandHandler

# === STEP 1: FILL THESE DETAILS ===
BOT_TOKEN = "PASTE_YOUR_TELEGRAM_BOT_TOKEN_HERE"
CONSUMER_KEY = "tI7C5MAnGpqy59AfwNNComn4uirateGYOtbUI9GaInvDaM2M"
CONSUMER_SECRET = "5jG2Wb9J4yGjKibfhgMYdfMnh2oEGXY9UIfSmrd9TLIL2kMnwU3D3k9kRnEToZ2o"
SHORTCODE = "174379"  # Daraja test shortcode (use your own if live)
PASSKEY = "cBJ5ggkfVrJK0fCn617+L9wWC0Y5/XuDCk6EwFWPp2AXJb/0hP+cnHCU3PwhCdOlHPw5J0DZwpUtmfKVDCJfBLGZU0ADxcYGJ1QYswSS/PTyt5GzqqtNvfdPRalksnPUvgzd0cLWHUKxkacxIZTm0Bg8iW5AO4KOfOT2cb8Lq68EPtWZTWfWpKeoASsET7BMSAySWQYxNWDPMjXhyZLysReqWDna/A4kN4tWPcBvRsilc7cSp/rbieb/u6AtYjmUcW8FeZCyzrbHY5/pHJE/+4j3UI0n1uVu5ZuavBGsVYwG48vtC0VTmVR3kG6Ruq91EoiMG1Cq681pP0BKCJvv7w=="

# === STEP 2: FUNCTION TO GET ACCESS TOKEN ===
def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET))
    return response.json()["access_token"]

# === STEP 3: FUNCTION TO TRIGGER MPESA STK PUSH ===
def stk_push(phone_number, amount):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((SHORTCODE + PASSKEY + timestamp).encode()).decode()
    access_token = get_access_token()

    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 100,
        "PartyA": phone_number,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://example.com/callback",
        "AccountReference": "TelegramBotPayment",
        "TransactionDesc": "Payment via Telegram Bot"
    }

    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )

    return response.json()

# === STEP 4: TELEGRAM BOT COMMANDS ===
async def paybill(update, context):
    await update.message.reply_text("Enter your phone number in format 2547XXXXXXXX.")
    # For now, just test with your own number
    phone = "254113869263"  # Replace with your number in sandbox
    result = stk_push(phone, 10)  # Amount = 100KES
    await update.message.reply_text(f"STK Push sent! Check your phone.\n\nResponse: {result}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("paybill", paybill))
    app.run_polling()

if __name__ == "__main__":
    main()
