#!/usr/bin/env python

import telegram

def main():
    token = '135793186:AAGZqxQeK0J0cwY3caNxM9eR9UD0vxh7Xvs'
    bot = telegram.Bot(token)
    update_id = 0
    while True:
        for update in bot.getUpdates(offset=update_id, timeout=60):
            update_id = update.update_id + 1
            bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text.encode('utf8'))

if __name__ == '__main__':
    main()

