import random
from aiogram import types
from aiogram.dispatcher import Dispatcher
import db
import config

async def spin_command(message: types.Message):
    user = db.get_user(message.from_user.id)
    if not user:
        db.add_user(message.from_user.id)

    # Предположим, что пользователь выбирает подарок на прокрутку через команду /spin <price>
    args = message.get_args()
    if not args.isdigit() or int(args) not in config.GIFTS:
        await message.answer("Выберите стоимость подарка из: " + ", ".join(map(str, config.GIFTS.keys())))
        return

    price = int(args)
    cost = config.spin_cost(price)
    aura_balance = db.get_aura(message.from_user.id)

    if aura_balance < cost:
        await message.answer(f"Недостаточно AURA для прокрута. Нужно: {cost} AURA")
        return

    # Списываем AURA
    db.update_aura(message.from_user.id, -cost)

    # Рандомим выигрыш
    win = random.randint(1, 100) <= config.WIN_CHANCE
    if win:
        gift = random.choice(config.GIFTS[price])
        db.add_gift(message.from_user.id, gift)
        await message.answer(f"Поздравляем! Вы выиграли подарок: {gift}")
    else:
        await message.answer("Увы, ничего не выиграли. Попробуйте ещё!")

def register_handlers_spin(dp: Dispatcher):
    dp.register_message_handler(spin_command, commands=["spin"])