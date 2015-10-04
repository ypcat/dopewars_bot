#!/usr/bin/env python

import os
import telegram
import dopewars

def main():
    token_file = os.path.join(os.path.dirname(__file__), 'token')
    bot = telegram.Bot(open(token_file).read().strip())
    update_id = 0
    while True:
        for update in bot.getUpdates(offset=update_id, timeout=60):
            try:
                update_id = update.update_id + 1
                chat_id = update.message.chat_id
                text = update.message.text.encode('utf8')
                name = update.message.from_user.name
                print name, text
                messages = dopewars.play(name, text)
                if messages:
                    text = '\n'.join(messages)
                    print text
                    bot.sendMessage(chat_id=chat_id, text=text)
            except:
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    main()
