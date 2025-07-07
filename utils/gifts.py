import random
from utils.aura import add_aura

GIFT_TIERS = {
    15: ["🧸", "💝"],
    25: ["🌹", "🎁"],
    50: ["🎂", "🚀"],
    100: ["🏆", "💎", "💍"]
}

SPIN_COST = lambda price: (price // 2) + (1 if price % 2 else 0)
SPIN_CHANCE = 0.45  # 45% шанс

def spin_gift(tier_price: int):
    success = random.random() < SPIN_CHANCE
    if success:
        gift = random.choice(GIFT_TIERS[tier_price])
        return gift
    return "❌"