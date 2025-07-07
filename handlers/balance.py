from aiogram import types
from aiogram.dispatcher import Dispatcher
import db

async def balance_command(message: types.Message):
    balance = db.get_aura(message.from_user.id)
    await message.answer(f"💰 Ваш баланс: {balance} ✨ AURA")

def register_handlers_balance(dp: Dispatcher):
    dp.register_message_handler(balance_command, commands=["balance"])