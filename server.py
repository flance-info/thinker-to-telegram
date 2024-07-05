from telegram import Bot

def send_file(token, chat_id, file_path):
    bot = Bot(token=token)
    with open(file_path, 'rb') as file:
        bot.send_document(chat_id=chat_id, document=file)
    print(f"File {file_path} sent successfully to chat ID {chat_id}")

if __name__ == '__main__':
    token = 'your_bot_token'
    chat_id = 'target_chat_id'
    file_path = 'path_to_your_file'
    send_file(token, chat_id, file_path)
