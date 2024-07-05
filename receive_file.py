import json
import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

def load_config(file):
    with open(file, 'r') as f:
        return json.load(f)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print('test')
    document = update.message.document
    file_id = document.file_id
    new_file = await context.bot.get_file(file_id)
    print('test')
    download_directory = context.bot_data['download_directory']
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    print(f"File {document.file_name} received with ID {file_id}")
    file_path = os.path.join(download_directory, document.file_name)
    print(file_path)
    await new_file.download_to_drive(file_path)
    await update.message.reply_text(f"File {document.file_name} received and downloaded to {file_path}")

async def main():
    config = load_config('config.json')
    print(config['bot_token'])
    application = Application.builder().token(config['bot_token']).build()
    application.bot_data['download_directory'] = config['download_directory']
    print(application.bot_data['download_directory'], filters.Document.ALL)
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

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

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped.")
