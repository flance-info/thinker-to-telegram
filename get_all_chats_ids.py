import json
import asyncio
from telethon import TelegramClient

# Load configuration
def load_config(file):
    with open(file, 'r') as f:
        return json.load(f)

async def send_message_as_user(config):
    api_id = config['api_id']
    api_hash = config['api_hash']
    phone_number = config['phone_number']
    chat_id = config['chat_id']
    message = config['message']

    client = TelegramClient('session_name', api_id, api_hash)

    await client.start(phone_number)

    # Fetch and print the list of dialogs to get correct chat IDs
    async for dialog in client.iter_dialogs():
        print(f'{dialog.name}: {dialog.id}')

    # Send message to the specified chat
    await client.send_message(chat_id, message)
    print(f"Message sent to chat ID {chat_id}.")

    await client.disconnect()

if __name__ == '__main__':
    config = load_config('config_user.json')
    asyncio.run(send_message_as_user(config))
