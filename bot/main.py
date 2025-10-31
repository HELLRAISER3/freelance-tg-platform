import asyncio
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, filters
)
from bot.handlers.start_handler import start
from bot.handlers.project_handler import (
    create_project_start,
    create_project_title,
    create_project_link,
    browse_projects,
    delete_project_command,
    navigate_page,
    bid_on_project,
    back_to_list,
    show_project_detail,
    PROJECT_TITLE,
    PROJECT_LINK
)
from bot.services.db_service import init_db
from bot.config import BOT_TOKEN

def run_bot_in_thread(application):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.run_polling()) # Await the coroutine
    loop.close()

def main():
    init_db()
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("delete", delete_project_command))

    post_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(create_project_start, pattern="create_project")],
        states={
            PROJECT_TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_project_title)],
            PROJECT_LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_project_link)],
        },
        fallbacks=[],
    )
    app.add_handler(post_conv)
    
    app.add_handler(CallbackQueryHandler(browse_projects, pattern="^browse_projects$"))
    app.add_handler(CallbackQueryHandler(navigate_page, pattern="^page_"))
    app.add_handler(CallbackQueryHandler(bid_on_project, pattern="^bid_"))
    app.add_handler(CallbackQueryHandler(back_to_list, pattern="^back_to_list$"))
    app.add_handler(CallbackQueryHandler(start, pattern="^back_to_main_menu"))
    app.add_handler(CallbackQueryHandler(show_project_detail, pattern="^project_view_"))



    print("🤖 Bot is running...")

    run_bot_in_thread(app)

if __name__ == "__main__": 
    main()


