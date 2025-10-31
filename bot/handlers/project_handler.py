from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
)
from bot.services.db_service import add_project, get_all_projects, delete_project
from bot.config import ADMIN_ID
import re
from datetime import datetime


PROJECT_TITLE, PROJECT_LINK = range(2)
TELEGRAPH_PATTERN = r"^https:\/\/telegra\.ph\/[a-zA-Z0-9\-_]+"
PROJECTS_PER_PAGE = 5


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

    project_id = add_project(title, link, update.effective_user.id)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Open Project", url=link)],
        [InlineKeyboardButton("Back", callback_data=f"back_to_main_menu")],
    ])

    await update.message.reply_text(
        f"✅ *Project successfully added to the stock!*\n\n"
        f"📌 *{title}*\n"
        f"Link: [Open Telegraph]({link})",
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=keyboard
    )
    return ConversationHandler.END

async def browse_projects(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point for browsing — always starts at page 0"""
    projects = get_all_projects()
    if not projects:
        await update.callback_query.message.reply_text("No projects yet 💤")
        return

    context.user_data["projects"] = projects
    await send_project_list(update, context, 0)


async def send_project_list(update: Update, context: ContextTypes.DEFAULT_TYPE, page: int):
    """Displays a list of projects as inline buttons"""
    projects = context.user_data.get("projects", [])
    total_pages = (len(projects) - 1) // PROJECTS_PER_PAGE + 1
    start = page * PROJECTS_PER_PAGE
    end = start + PROJECTS_PER_PAGE
    subset = projects[start:end]

    keyboard = []
    for pid, title, link, date in subset:
        keyboard.append([InlineKeyboardButton(title, callback_data=f"project_view_{pid}")])


    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton("⬅ Prev", callback_data=f"page_{page-1}"))
    if page < total_pages - 1:
        nav_buttons.append(InlineKeyboardButton("Next ➡", callback_data=f"page_{page+1}"))
    if nav_buttons:
        keyboard.append(nav_buttons)
        
    keyboard.append([InlineKeyboardButton("Back", callback_data=f"back_to_main_menu")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "📢 *Recent Projects:*"

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=text, parse_mode="Markdown", reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

async def navigate_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    page = int(query.data.split("_")[1])
    await send_project_list(update, context, page)


async def show_project_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    pid = int(query.data.split("_")[2])

    projects = context.user_data.get("projects", [])

    project = next((p for p in projects if p[0] == pid), None)

    if not project:
        await query.message.reply_text("Project not found ❌")
        return

    pid, title, link, date = project
    text = (
        f"🧩 *{title}*\n\n"
        f"🔗 [View on Telegraph]({link})\n"
        f"📅 Created: `{date}`"
    )

    keyboard = [
        [InlineKeyboardButton("💸 Bid", callback_data=f"bid_{pid}")],
        [InlineKeyboardButton("⬅ Back to list", callback_data="back_to_list")]
    ]

    await query.edit_message_text(
        text=text,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def back_to_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await send_project_list(update, context, 0)

async def bid_on_project(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pid = int(query.data.split("_")[1])
    await query.message.reply_text(f"💬 You clicked to bid on project ID {pid}. (Coming soon...)")


# --- Delete project (admin only) ---

async def delete_project_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Access denied")
        return
    try:
        pid = int(context.args[0])
        delete_project(pid)
        await update.message.reply_text("✅ Project deleted")
    except Exception:
        await update.message.reply_text("Usage: /delete <project_id>")


# --- Bid button callback stub (placeholder for future logic) ---

async def bid_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    project_id = int(query.data.split("_")[1])
    await query.answer()
    await query.message.reply_text(
        f"💰 You pressed *Bid* for project ID: {project_id}.\n\n"
        f"(Bidding logic will go here.)", parse_mode="Markdown"
    )
