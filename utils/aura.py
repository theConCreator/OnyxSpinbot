from db import get_user, update_user_balance

def add_aura(user_id: int, amount: float):
    user = get_user(user_id)
    if user:
        new_balance = user['aura'] + amount
        update_user_balance(user_id, new_balance)

def subtract_aura(user_id: int, amount: float) -> bool:
    user = get_user(user_id)
    if user and user['aura'] >= amount:
        new_balance = user['aura'] - amount
        update_user_balance(user_id, new_balance)
        return True
    return False

def get_aura(user_id: int) -> float:
    user = get_user(user_id)
    return user['aura'] if user else 0