from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📄 View Projects")],
        [InlineKeyboardButton("📝 Post a Project")],
        [InlineKeyboardButton("💼 My Profile")],
        [InlineKeyboardButton("⚙️ Settings")],
    ]
    return InlineKeyboardMarkup(keyboard)

