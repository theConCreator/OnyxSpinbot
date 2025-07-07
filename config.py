import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "8032705985:AAG0RbZMv0xMKJnqdIdh7Eyn-9Lr_YUKjKE")

# Стоимости подарков
GIFTS = {
    15: ["мишка🧸", "сердце💝"],
    25: ["роза🌹", "подарок🎁"],
    50: ["торт🎂", "ракета🚀"],
    100: ["кубок🏆", "алмаз💎", "кольцо💍"]
}

# Цена прокрута — половина стоимости подарка с округлением вверх
def spin_cost(price: int) -> int:
    return (price + 1) // 2

# Вероятность выигрыша (в процентах)
WIN_CHANCE = 45

# Комиссия при пополнении AURA звёздами
AURA_STAR_COMMISSION = 0.14

# Курс AURA (за 1 AURA)
AURA_TO_USDT = 0.017
AURA_TO_TON = 0.0058

# Админ ID (для команд админа)
ADMIN_IDS = {123456789}  # замените на свой ID