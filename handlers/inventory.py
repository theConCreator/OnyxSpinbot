from aiogram import types
from aiogram.dispatcher import Dispatcher
import db

async def inventory_command(message: types.Message):
    items = db.get_inventory(message.from_user.id)
    if not items:
        await message.answer("Ваш инвентарь пуст.")
        return

    text = "Ваш инвентарь:\n"
    for item_id, gift in items:
        text += f"ID: {item_id} — {gift}\n"

    await message.answer(text)

def register_handlers_inventory(dp: Dispatcher):
    dp.register_message_handler(inventory_command, commands=["inventory"])