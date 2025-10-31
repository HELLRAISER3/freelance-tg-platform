from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from bot.services.db_service import add_project, get_projects, delete_project
from bot.config import ADMIN_ID
import re

PROJECT_TITLE, PROJECT_LINK = range(2)

TELEGRAPH_PATTERN = r"^https:\/\/telegra\.ph\/[a-zA-Z0-9\-_]+"

# --- Create project flow ---

async def create_project_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text(
        "📝 Send me the *title* of your project (short summary):", parse_mode="Markdown"
    )
    return PROJECT_TITLE


async def create_project_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text
    await update.message.reply_text(
        "Now send me the *Telegraph link* (e.g. https://telegra.ph/your-post):",
        parse_mode="Markdown"
    )
    return PROJECT_LINK


async def create_project_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    link = update.message.text.strip()
    title = context.user_data["title"]

    if not re.match(TELEGRAPH_PATTERN, link):
        await update.message.reply_text("⚠️ Please send a valid Telegraph link (starts with https://telegra.ph/)")
        return PROJECT_LINK

    add_project(title, link, update.effective_user.id)
    await update.message.reply_text("✅ Project successfully added to the stock!")
    return ConversationHandler.END


# --- Browse projects ---

async def browse_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    projects = get_projects()
    if not projects:
        await update.callback_query.message.reply_text("No projects yet 💤")
        return

    text = "📢 *Latest Projects:*\n\n"
    for pid, title, link, date in projects:
        text += f"• [{title}]({link})\n"
    await update.callback_query.message.reply_text(text, parse_mode="Markdown", disable_web_page_preview=True)
async def delete_project_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Access denied")
        return
    try:
        pid = int(context.args[0])
        delete_project(pid)
        await update.message.reply_text("✅ Project deleted")
    except Exception as e:
        await update.message.reply_text("Usage: /delete <project_id>")