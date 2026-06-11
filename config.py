import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
DB_PATH = os.getenv("DB_PATH", "bot.db")

# حداقل سکه برای دریافت کانفیگ رایگان
MIN_COINS_FOR_FREE_CONFIG = 5

# نام ربات (برای ساخت لینک دعوت - اگر ست نشود از get_me استفاده می‌شود)
BOT_USERNAME = os.getenv("BOT_USERNAME", "")
