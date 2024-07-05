import socket
import win32clipboard
from PIL import ImageGrab, Image
from io import BytesIO
import keyboard
import time
import struct
import requests
from userbot import main


def get_clipboard_image():
    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(win32clipboard.CF_DIB)
        win32clipboard.CloseClipboard()

        image = ImageGrab.grabclipboard()
        if image is None:
            print("No image found in clipboard.")
            return
    except TypeError:
        image = None

    return image

def send_screenshot():
   # Give some time for the screenshot to be copied to the clipboard
    time.sleep(1)
    screenshot = get_clipboard_image()
    if screenshot is None:
        print("No image found in clipboard.")
        return

    buffer = BytesIO()
    screenshot.save(buffer, format='PNG')
    buffer.seek(0)

    files = {'file': ('screenshot.png', buffer, 'image/png')}

    try:
      response = main(files)
    except ConnectionRefusedError:
        print("Failed to connect to the server. Make sure the server is running.")

if __name__ == "__main__":

    print("Press Alt + Print Screen to send a screenshot from clipboard")
    keyboard.add_hotkey('alt+print_screen', lambda: send_screenshot())

    # Keep the script running
    keyboard.wait('esc')  # Press 'Esc' to stop the script
