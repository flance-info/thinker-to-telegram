from telegram.ext import Updater, MessageHandler, Filters

def handle_document(update, context):
    document = update.message.document
    file_id = document.file_id
    new_file = context.bot.get_file(file_id)
    new_file.download(f'downloaded_{document.file_name}')
    update.message.reply_text(f"File {document.file_name} received and downloaded.")

def main():
    token = 'your_bot_token'
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.document, handle_document))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
