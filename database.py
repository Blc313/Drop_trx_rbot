import sqlite3
import threading
from datetime import datetime
from config import DB_PATH

_lock = threading.Lock()


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with _lock, get_conn() as conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT,
            join_date TEXT,
            coins INTEGER DEFAULT 0,
            invites INTEGER DEFAULT 0,
            referrer_id INTEGER
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount TEXT,
            status TEXT DEFAULT 'pending',
            receipt_file_id TEXT,
            created_at TEXT,
            reject_reason TEXT,
            config_text TEXT
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            config_text TEXT,
            used INTEGER DEFAULT 0
        )
        """)
        c.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)
        # مقادیر پیش‌فرض تنظیمات
        defaults = {
            "card_number": "0000-0000-0000-0000",
            "card_holder": "نام صاحب کارت",
            "rules_text": "قوانین ربات هنوز تنظیم نشده است.",
            "support_text": "برای ارتباط با پشتیبانی، پیام خود را همینجا ارسال کنید.",
            "product_price": "400,000 تومان",
        }
        for k, v in defaults.items():
            c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)", (k, v))
        conn.commit()


# ---------------- Users ----------------

def get_user(user_id: int):
    with _lock, get_conn() as conn:
        return conn.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchone()


def create_user(user_id: int, full_name: str, username: str, referrer_id: int = None):
    with _lock, get_conn() as conn:
        conn.execute(
            "INSERT INTO users (user_id, full_name, username, join_date, coins, invites, referrer_id) "
            "VALUES (?, ?, ?, ?, 0, 0, ?)",
            (user_id, full_name, username, datetime.now().isoformat(), referrer_id),
        )
        conn.commit()


def add_coins(user_id: int, amount: int):
    with _lock, get_conn() as conn:
        conn.execute("UPDATE users SET coins = coins + ? WHERE user_id=?", (amount, user_id))
        conn.commit()


def increment_invites(user_id: int):
    with _lock, get_conn() as conn:
        conn.execute("UPDATE users SET invites = invites + 1 WHERE user_id=?", (user_id,))
        conn.commit()


def deduct_coins(user_id: int, amount: int) -> bool:
    with _lock, get_conn() as conn:
        row = conn.execute("SELECT coins FROM users WHERE user_id=?", (user_id,)).fetchone()
        if not row or row["coins"] < amount:
            return False
        conn.execute("UPDATE users SET coins = coins - ? WHERE user_id=?", (amount, user_id))
        conn.commit()
        return True


# ---------------- Configs (بانک کانفیگ رایگان) ----------------

def add_config(text: str):
    with _lock, get_conn() as conn:
        conn.execute("INSERT INTO configs (config_text, used) VALUES (?, 0)", (text,))
        conn.commit()


def get_random_unused_config():
    with _lock, get_conn() as conn:
        row = conn.execute("SELECT * FROM configs WHERE used=0 ORDER BY RANDOM() LIMIT 1").fetchone()
        if row:
            conn.execute("UPDATE configs SET used=1 WHERE id=?", (row["id"],))
            conn.commit()
        return row


def count_available_configs():
    with _lock, get_conn() as conn:
        row = conn.execute("SELECT COUNT(*) as cnt FROM configs WHERE used=0").fetchone()
        return row["cnt"]


# ---------------- Orders ----------------

def create_order(user_id: int, amount: str, receipt_file_id: str) -> int:
    with _lock, get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO orders (user_id, amount, status, receipt_file_id, created_at) "
            "VALUES (?, ?, 'pending', ?, ?)",
            (user_id, amount, receipt_file_id, datetime.now().isoformat()),
        )
        conn.commit()
        return cur.lastrowid


def get_order(order_id: int):
    with _lock, get_conn() as conn:
        return conn.execute("SELECT * FROM orders WHERE order_id=?", (order_id,)).fetchone()


def get_pending_orders():
    with _lock, get_conn() as conn:
        return conn.execute("SELECT * FROM orders WHERE status='pending' ORDER BY order_id ASC").fetchall()


def get_user_orders(user_id: int):
    with _lock, get_conn() as conn:
        return conn.execute(
            "SELECT * FROM orders WHERE user_id=? ORDER BY order_id DESC", (user_id,)
        ).fetchall()


def approve_order(order_id: int, config_text: str):
    with _lock, get_conn() as conn:
        conn.execute(
            "UPDATE orders SET status='completed', config_text=? WHERE order_id=?",
            (config_text, order_id),
        )
        conn.commit()


def reject_order(order_id: int, reason: str):
    with _lock, get_conn() as conn:
        conn.execute(
            "UPDATE orders SET status='rejected', reject_reason=? WHERE order_id=?",
            (reason, order_id),
        )
        conn.commit()


# ---------------- Settings ----------------

def get_setting(key: str) -> str:
    with _lock, get_conn() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row["value"] if row else ""


def set_setting(key: str, value: str):
    with _lock, get_conn() as conn:
        conn.execute("INSERT INTO settings (key, value) VALUES (?, ?) "
                      "ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, value))
        conn.commit()
