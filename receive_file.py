import json
import os
import asyncio
import logging
from telegram import ForceReply, Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from clipboard import send_to_clipboard  # Changed to absolute import
import win32clipboard
from io import BytesIO
from PIL import Image

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
    
    try:
        with Image.open(file_path) as image:
            output = BytesIO()
            image.convert('RGB').save(output, format='BMP')
            data = output.getvalue()[14:]
            output.close()

        send_to_clipboard(win32clipboard.CF_DIB, data)
        print("Screenshot copied to clipboard!")
    except Exception as e:
        print(f"Error processing image: {e}")
        await update.message.reply_text(f"Failed to process the file {document.file_name}")

    await update.message.reply_text(f"File {document.file_name} received and downloaded to {file_path}")

# Photo handler
async def handle_document_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    photo = update.message.photo
    if not photo:
        await update.message.reply_text('No photo found in the message.')
        return

    # Get the highest resolution photo (last in the list)
    photo = photo[-1]
    file_id = photo.file_id

    # Get the file
    new_file = await context.bot.get_file(file_id)
    file_path = new_file.file_path

    # Download the file
    await new_file.download_to_drive(f'./downloaded_files/photo_{file_id}.png')
    try:
        with Image.open(new_file) as image:
            output = BytesIO()
            image.convert('RGB').save(output, format='BMP')
            data = output.getvalue()[14:]
            output.close()

        send_to_clipboard(win32clipboard.CF_DIB, data)
        print("Screenshot copied to clipboard!")
    except Exception as e:
        print(f"Error processing image: {e}")
        await update.message.reply_text(f"Failed to process the file {document.file_name}")
   
    await update.message.reply_text('Photo downloaded successfully.')

async def main():
    config = load_config('config.json')
    application = Application.builder().token(config['bot_token']).build()
    application.bot_data['download_directory'] = config['download_directory']

    # Add handlers
   
    application.add_handler(MessageHandler(filters.PHOTO, handle_document_photo))
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

      
