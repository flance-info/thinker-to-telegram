import json
import asyncio
from telethon import TelegramClient
from io import BytesIO
from PIL import ImageGrab, Image
import time
import keyboard

# Load configuration
def load_config(file):
    with open(file, 'r') as f:
        return json.load(f)

async def send_file(file, config):
    api_id = config['api_id']
    api_hash = config['api_hash']
    phone_number = config['phone_number']
    username = config['username']

    client = TelegramClient('session_name', api_id, api_hash)
    await client.start(phone_number)

    # Get the user entity
    entity = await client.get_entity(username)
    
    # Send the file
    await client.send_file(entity, file)
    print(f"File sent successfully to {username}.")

    await client.disconnect()

def main(file): 
    config = load_config('config.json')
    asyncio.run(send_file(file, config))

def get_clipboard_image():
    try:
        image = ImageGrab.grabclipboard()
        if isinstance(image, Image.Image):
            return image
    except Exception as e:
        print(f"Error grabbing image from clipboard: {e}")
    return None

def send_screenshot():
    print("Capturing the active window...")
    
    # Give some time for the screenshot to be copied to the clipboard
    time.sleep(1)
    
    screenshot = get_clipboard_image()
    if screenshot is None:
        print("No image found in clipboard.")
        return

    buffer = BytesIO()
    screenshot.save(buffer, format='PNG')
    buffer.seek(0)

    try:
        main(buffer)
    except Exception as e:
        print(f"Error sending screenshot: {e}")

if __name__ == "__main__":

    print("Press Alt + Print Screen to send a screenshot from clipboard")
    keyboard.add_hotkey('alt+print_screen', lambda: send_screenshot())

    # Keep the script running
    keyboard.wait('esc')  # Press 'Esc' to stop the script
