import json
import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

def load_config(file):
    with open(file, 'r') as f:
        return json.load(f)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    file_id = document.file_id
    new_file = await context.bot.get_file(file_id)
    
    download_directory = context.bot_data['download_directory']
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    
    file_path = os.path.join(download_directory, document.file_name)
    await new_file.download_to_drive(file_path)
    await update.message.reply_text(f"File {document.file_name} received and downloaded to {file_path}")

async def main():
    config = load_config('config.json')
    application = Application.builder().token(config['bot_token']).build()
    application.bot_data['download_directory'] = config['download_directory']
    
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Start polling
    await application.start()
    application.updater.start_polling()
    print("Bot is running. Press Ctrl+C to stop.")

    # Create an event to keep the script running
    await application.updater._request.stop.wait()

    # Graceful shutdown
    await application.stop()
    await application.shutdown()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")

