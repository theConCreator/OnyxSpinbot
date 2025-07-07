from aiogram import types
from aiogram.dispatcher import Dispatcher
import db

async def referrals_command(message: types.Message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    if not user:
        db.add_user(user_id)

    ref_link = f"https://t.me/{db.get_bot_username()}?start={user_id}"
    total_earned = db.get_referral_earnings(user_id)

    await message.answer(
        f"👥 Ваша реферальная ссылка:\n{ref_link}\n\n"
        f"💸 Вы заработали с рефералов: {total_earned} AURA\n\n"
        f"🎁 Введите промокод, если он у вас есть, чтобы получить бонус.\n"
        f"Пример: /promo MYCODE"
    )

async def promo_command(message: types.Message):
    code = message.get_args().strip().upper()
    if not code:
        await message.answer("Введите промокод, например: /promo GIFT100")
        return

    result = db.redeem_promocode(message.from_user.id, code)
    await message.answer(result)

def register_handlers_referrals(dp: Dispatcher):
    dp.register_message_handler(referrals_command, commands=["ref"])
    dp.register_message_handler(promo_command, commands=["promo"])