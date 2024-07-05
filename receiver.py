import json
import logging
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Load configuration
def load_config(file):
    with open(file, 'r') as f:
        return json.load(f)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send me a file and I will download it for you.')

# Document handler
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    document = update.message.document
    file_id = document.file_id

    # Get the file
    new_file = await context.bot.get_file(file_id)
    file_path = new_file.file_path

    # Download the file
    await new_file.download_to_drive(f'./downloaded_files/{document.file_name}')
    await update.message.reply_text(f'File {document.file_name} downloaded successfully.')

# Main function to run the bot
def main():
    # Set up logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Load config
    config = load_config('config.json')
    bot_token = config['bot_token']

    # Set up the Application
    application = Application.builder().token(bot_token).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
