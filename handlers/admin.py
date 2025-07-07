from aiogram import types
from aiogram.dispatcher import Dispatcher
import db
import config

ADMIN_ID = config.ADMIN_ID  # укажите ваш Telegram ID в config.py

async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "🛠 Админ-панель:\n"
        "/aura_stats - Статистика покупок AURA\n"
        "/promo_create CODE COUNT AMOUNT - Создать промо\n"
        "/withdraw_requests - Запросы на вывод подарков"
    )

async def aura_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    stats = db.get_aura_stats()
    await message.answer(
        f"💰 Статистика AURA:\n"
        f"— Через звезды: {stats['stars']} AURA\n"
        f"— Через TON: {stats['ton']} AURA\n"
        f"— Через USDT: {stats['usdt']} AURA"
    )

async def promo_create(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    args = message.get_args().split()
    if len(args) != 3:
        await message.answer("Формат: /promo_create CODE COUNT AMOUNT")
        return

    code, count, amount = args
    db.create_promocode(code.upper(), int(count), int(amount))
    await message.answer(f"✅ Промокод {code} создан")

async def withdraw_requests(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    requests = db.get_withdraw_requests()
    if not requests:
        await message.answer("Нет активных запросов на вывод.")
        return

    response = "📤 Запросы на вывод:\n"
    for req in requests:
        user_id, item_id, gift = req
        tg_link = f"tg://openmessage?user_id={user_id}"
        response += f"{gift} (ID: {item_id}) от [{user_id}]({tg_link})\n"

    await message.answer(response, parse_mode="Markdown")

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(admin_panel, commands=["admin"])
    dp.register_message_handler(aura_stats, commands=["aura_stats"])
    dp.register_message_handler(promo_create, commands=["promo_create"])
    dp.register_message_handler(withdraw_requests, commands=["withdraw_requests"])