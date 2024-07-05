import json
import os
from telegram.ext import Updater, MessageHandler, Filters

def load_config(file):
    with open(file, 'r') as f:
        return json.load(f)

def handle_document(update, context):
    document = update.message.document
    file_id = document.file_id
    new_file = context.bot.get_file(file_id)
    
    # Ensure download directory exists
    download_directory = context.bot_data['download_directory']
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    
    file_path = os.path.join(download_directory, document.file_name)
    new_file.download(file_path)
    update.message.reply_text(f"File {document.file_name} received and downloaded to {file_path}")

def main():
    config = load_config('config.json')
    updater = Updater(config['bot_token'], use_context=True)
    dp = updater.dispatcher
    dp.bot_data['download_directory'] = config['download_directory']
    dp.add_handler(MessageHandler(Filters.document, handle_document))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
