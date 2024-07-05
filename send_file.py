import json
from telegram import Bot

def load_config(file):
    with open(file, 'r') as f:
        return json.load(f)

def send_file(config):
    bot = Bot(token=config['bot_token'])
    with open(config['file_path'], 'rb') as file:
        bot.send_document(chat_id=config['chat_id'], document=file)
    print(f"File {config['file_path']} sent successfully to chat ID {config['chat_id']}")

if __name__ == '__main__':
    config = load_config('config.json')
    send_file(config)
