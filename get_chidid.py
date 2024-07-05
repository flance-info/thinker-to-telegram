import requests

def get_updates(bot_token):
    url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    response = requests.get(url)
    return response.json()

def main():
    bot_token = '7465085737:AAHiFAH8ZtldPXrhCShKgvObbttfvdoyehY'  # Replace with your bot token
    updates = get_updates(bot_token)

    if 'result' in updates and len(updates['result']) > 0:
        chat_id = updates['result'][0]['message']['chat']['id']
        print(f"Your chat ID is: {chat_id}")
    else:
        print("No messages found. Please send a message to your bot first.")

if __name__ == '__main__':
    main()
