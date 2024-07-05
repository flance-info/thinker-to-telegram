import json
import asyncio
from telethon import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChat, InputPeerChannel

# Load configuration
def load_config(file):
    with open(file, 'r') as f:
        return json.load(f)

async def send_file(config):
    api_id = config['api_id']
    api_hash = config['api_hash']
    phone_number = config['phone_number']
    username = config['username']
    file_path = config['file_path']

    client = TelegramClient('session_name', api_id, api_hash)
    await client.start(phone_number)

    # Get the user entity
    entity = await client.get_entity(username)
    
    # Send the file
    await client.send_file(entity, file_path)
    print(f"File {file_path} sent successfully to {username}.")

    await client.disconnect()

if __name__ == '__main__':
    config = load_config('config.json')
    asyncio.run(send_file(config))
