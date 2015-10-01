#!/usr/bin/env python

import telegram

from dopewars import start, is_finish, get_message, process

def main():
    token = '135793186:AAGZqxQeK0J0cwY3caNxM9eR9UD0vxh7Xvs'
    bot = telegram.Bot(token)
    update_id = 0
    sessions = {}
    while True:
        for update in bot.getUpdates(offset=update_id, timeout=60):
            try:
                update_id = update.update_id + 1
                chat_id = update.message.chat_id
                input = update.message.text.encode('utf8')
                text = ''
                if input == 'start':
                    id = start(update.from_user.name)
                    sessions[chat_id] = id
                    text = get_message(id)
                elif chat_id in sessions and process(sessions[chat_id], input):
                    text = get_message(id)
                if text:
                    bot.sendMessage(chat_id=chat_id, text=text)
            except:
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    main()

