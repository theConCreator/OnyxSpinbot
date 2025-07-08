import sys
import os

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(file), '..')))

from aiohttp import web
import json
import asyncio
from utils.aura import add_aura
from config import TELEGRAM_BOT_TOKEN, CRYPTOBOT_TOKEN
from db import get_user, create_user
from aiogram import Bot, Dispatcher, types

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

routes = web.RouteTableDef()

@routes.post("/telegram-webhook")
async def telegram_webhook(request):
    data = await request.json()
    update = types.Update(**data)
    await dp.process_update(update)
    return web.Response()

@routes.post("/cryptobot-webhook")
async def cryptobot_webhook(request):
    data = await request.json()
    
    if data.get("event") != "invoice_paid":
        return web.Response(status=200)
    
    payload = data.get("payload")
    if not payload or ":" not in payload:
        return web.Response(status=400)
    
    action, user_id = payload.split(":")
    user_id = int(user_id)
    amount = float(data["amount"])
    asset = data["asset"]

    # Переводим валюту в AURA
    aura_amount = 0
    if asset == "USDT":
        aura_amount = round(amount / 0.017, 2)
    elif asset == "TON":
        aura_amount = round(amount / 0.0058, 2)

    if aura_amount > 0:
        create_user(user_id)
        add_aura(user_id, aura_amount)

        await bot.send_message(
            user_id,
            f"✅ Пополнение успешно! Зачислено {aura_amount} AURA 💫"
        )

    return web.Response(status=200)

def run_server():
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host="0.0.0.0", port=8080)

if __name__ == "__main__":
    run_server()