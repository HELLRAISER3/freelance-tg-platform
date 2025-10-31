from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📄 View Projects", callback_data='browse_projects')],
        [InlineKeyboardButton("📝 Post a Project", callback_data='create_projects')], 
        [InlineKeyboardButton("💼 My Profile", callback_data='my_profile')],
        [InlineKeyboardButton("⚙️ Settings", callback_data='settings')],
    ]
    return InlineKeyboardMarkup(keyboard)

