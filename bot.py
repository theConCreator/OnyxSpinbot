import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import db

from handlers import (
    start, spin, inventory, referrals, admin, balance
)

start.register_handlers_start(dp)
spin.register_handlers_spin(dp)
inventory.register_handlers_inventory(dp)
referrals.register_handlers_referrals(dp)
admin.register_handlers_admin(dp)
balance.register_handlers_balance(dp)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        db.add_user(message.from_user.id)
    await message.answer("Добро пожаловать в AuraGiftBot! Используйте /spin для прокрутки.")

@dp.message_handler(commands=["balance"])
async def balance_handler(message: types.Message):
    aura = db.get_aura(message.from_user.id)
    await message.answer(f"Ваш баланс: {aura} AURA ✨️")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)