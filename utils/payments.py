import requests
from config import CRYPTOBOT_TOKEN, BOT_USERNAME

API_URL = f"https://pay.crypt.bot/api"

def create_invoice(amount_usdt: float, user_id: int, currency="USDT", payload="topup"):
    headers = {
        "Crypto-Pay-API-Token": CRYPTOBOT_TOKEN
    }

    data = {
        "asset": currency,
        "amount": amount_usdt,
        "description": f"AURA пополнение для @{BOT_USERNAME}",
        "hidden_message": f"Пополнение {amount_usdt} {currency}",
        "payload": f"{payload}:{user_id}",
        "allow_comments": False,
        "allow_anonymous": False
    }

    response = requests.post(f"{API_URL}/createInvoice", headers=headers, json=data)
    if response.ok:
        return response.json()["result"]["pay_url"]
    else:
        return None