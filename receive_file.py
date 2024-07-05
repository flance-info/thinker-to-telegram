import json
import os
import asyncio
import logging
from telegram import ForceReply, Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

def load_config(file):
    with open(file, 'r') as f:
        return json.load(f)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    print(update.message.text)
    await update.message.reply_text(update.message.text)

    
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("handle_document triggered")
    document = update.message.document
    file_id = document.file_id
    new_file = await context.bot.get_file(file_id)
    
    download_directory = context.bot_data['download_directory']
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    
    file_path = os.path.join(download_directory, document.file_name)
    await new_file.download_to_drive(file_path)
    await update.message.reply_text(f"File {document.file_name} received and downloaded to {file_path}")

async def debug_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Received update: {update}")

async def main():
    config = load_config('config.json')
    application = Application.builder().token(config['bot_token']).build()
    application.bot_data['download_directory'] = config['download_directory']

    # Add handlers
    application.add_handler(MessageHandler(filters.ALL, debug_update))
    application.add_handler(MessageHandler(filters.All, handle_document))
    

    # Initialize and start the application
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    print("Bot is running. Press Ctrl+C to stop.")

    # Wait for a shutdown signal (Ctrl+C)
    try:
        await asyncio.Future()  # Run forever
    except asyncio.CancelledError:
        print("Bot is stopping...")
    finally:
        await application.updater.stop()  # Stop the updater before shutdown
        await application.stop()
        await application.shutdown()
        print("Bot stopped.")



def mainstart() -> None:
    config = load_config('config.json')
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config['bot_token']).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

""" 
if __name__ == "__main__":
    mainstart() 
"""
if __name__ == '__main__':
    try:
       asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")   

      
