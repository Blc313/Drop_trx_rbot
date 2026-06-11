from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# ---------------- منوی اصلی کاربر ----------------

def main_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎁 دریافت کانفیگ رایگان"), KeyboardButton(text="👥 دعوت دوستان")],
            [KeyboardButton(text="💰 موجودی سکه"), KeyboardButton(text="💳 خرید اشتراک")],
            [KeyboardButton(text="📦 سفارش‌های من"), KeyboardButton(text="📜 قوانین")],
            [KeyboardButton(text="☎️ پشتیبانی")],
        ],
        resize_keyboard=True,
    )
    return kb


def back_to_menu_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 بازگشت به منو")]],
        resize_keyboard=True,
    )


def confirm_payment_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="✅ پرداخت کردم", callback_data="paid")]]
    )


def cancel_inline_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="❌ انصراف", callback_data="cancel_action")]]
    )


# ---------------- پنل مدیریت ----------------

def admin_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📥 سفارش‌های در انتظار", callback_data="admin_pending")],
            [InlineKeyboardButton(text="💳 تنظیم اطلاعات پرداخت", callback_data="admin_set_payment")],
            [InlineKeyboardButton(text="📜 ویرایش قوانین", callback_data="admin_set_rules")],
            [InlineKeyboardButton(text="➕ افزودن کانفیگ رایگان", callback_data="admin_add_config")],
            [InlineKeyboardButton(text="📊 آمار ربات", callback_data="admin_stats")],
        ]
    )


def admin_order_actions_kb(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ تایید سفارش", callback_data=f"approve_{order_id}"),
                InlineKeyboardButton(text="❌ رد سفارش", callback_data=f"reject_{order_id}"),
            ]
        ]
    )


def back_to_admin_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔙 بازگشت به پنل ادمین", callback_data="admin_back")]]
    )
