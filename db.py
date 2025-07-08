import sqlite3
from contextlib import closing

conn = sqlite3.connect("aura_gift_bot.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    with closing(conn.cursor()) as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                aura INTEGER DEFAULT 0,
                referrer_id INTEGER
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                gift TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER,
                referred_id INTEGER,
                total_referred_aura INTEGER DEFAULT 0
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS promo_codes (
                code TEXT PRIMARY KEY,
                aura_amount INTEGER,
                uses_left INTEGER
            )
        """)
        conn.commit()

DB_NAME = "aura.db"

def update_user_balance(user_id: int, new_balance: int):
    with sqlite3.connect(DB_NAME) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET aura = ? WHERE user_id = ?", (new_balance, user_id))
        conn.commit()

def get_user(user_id):
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT user_id, aura, referrer_id FROM users WHERE user_id = ?", (user_id,))
        return cur.fetchone()

def add_user(user_id, referrer_id=None):
    with closing(conn.cursor()) as cur:
        cur.execute("INSERT OR IGNORE INTO users (user_id, referrer_id) VALUES (?, ?)", (user_id, referrer_id))
        conn.commit()

def update_aura(user_id, amount):
    with closing(conn.cursor()) as cur:
        cur.execute("UPDATE users SET aura = aura + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()

def get_aura(user_id):
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT aura FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return row[0] if row else 0

def add_gift(user_id, gift):
    with closing(conn.cursor()) as cur:
        cur.execute("INSERT INTO inventory (user_id, gift) VALUES (?, ?)", (user_id, gift))
        conn.commit()

def get_inventory(user_id):
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT id, gift FROM inventory WHERE user_id = ?", (user_id,))
        return cur.fetchall()

def remove_gift(inv_id):
    with closing(conn.cursor()) as cur:
        cur.execute("DELETE FROM inventory WHERE id = ?", (inv_id,))
        conn.commit()

def get_promo_code(code):
    with closing(conn.cursor()) as cur:
        cur.execute("SELECT code, aura_amount, uses_left FROM promo_codes WHERE code = ?", (code,))
        return cur.fetchone()

def use_promo_code(code):
    with closing(conn.cursor()) as cur:
        cur.execute("UPDATE promo_codes SET uses_left = uses_left - 1 WHERE code = ?", (code,))
        conn.commit()

def create_promo_code(code, aura_amount, uses):
    with closing(conn.cursor()) as cur:
        cur.execute("INSERT INTO promo_codes (code, aura_amount, uses_left) VALUES (?, ?, ?)",
                    (code, aura_amount, uses))
        conn.commit()

init_db()