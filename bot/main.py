import asyncio
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters
)
from bot.handlers.start_handler import start
from bot.handlers.project_handler import (
    post_project_start,
    post_project_title,
    post_project_description,
    browse_projects,
    delete_project_command,
    POST_TITLE,
    POST_DESC
)
from bot.services.db_service import init_db
from bot.config import BOT_TOKEN

def main():
    init_db()
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("delete", delete_project_command))

    post_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(post_project_start, pattern="post_project")],
        states={
            POST_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, post_project_title)],
            POST_DESC: [MessageHandler(filters.TEXT & ~filters.COMMAND, post_project_description)],
        },
        fallbacks=[],
    )
    app.add_handler(post_conv)
    app.add_handler(CallbackQueryHandler(browse_projects, pattern="browse_projects"))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__": 
    main()
