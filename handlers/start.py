from aiogram import types
from aiogram.dispatcher import Dispatcher
import db

async def start_command(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        db.add_user(message.from_user.id, referrer_id=None)
    await message.answer(
        "Добро пожаловать в AuraGiftBot!\n"
        "Выберите действие:\n"
        "/spin - Сделать прокрут\n"
        "/inventory - Посмотреть инвентарь\n"
        "/balance - Узнать баланс AURA"
    )

def register_handlers_start(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=["start"])