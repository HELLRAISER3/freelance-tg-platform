from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from bot.services.db_service import add_project, get_projects, delete_project
from bot.config import ADMIN_ID

POST_TITLE, POST_DESC = range(2)

async def post_project_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.message.reply_text("📝 Send me the *title* of your project:", parse_mode="Markdown")
    return POST_TITLE

async def post_project_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["title"] = update.message.text
    await update.message.reply_text("Now send me the *description*:", parse_mode="Markdown")
    return POST_DESC

async def post_project_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    title = context.user_data["title"]
    desc = update.message.text
    add_project(title, desc, update.effective_user.id)
    await update.message.reply_text("✅ Project posted successfully!")
    return ConversationHandler.END

async def browse_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    projects = get_projects()
    if not projects:
        await update.callback_query.message.reply_text("No projects yet 💤")
        return
    text = "\n\n".join([f"📌 *{t}*\n{d}" for _, t, d in projects])
    await update.callback_query.message.reply_text(text, parse_mode="Markdown")

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