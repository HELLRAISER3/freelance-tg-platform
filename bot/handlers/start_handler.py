from telegram import Update
from telegram.ext import ContextTypes
from bot.services.db_service import add_user
from bot.keyboards.main_menu import main_menu_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username or "unknown")
    await update.message.reply_text(
        f"👋 Hello, {user.first_name}! Welcome to Freelance Bot.\nChoose an option:",
        reply_markup=main_menu_keyboard()
    )
    
