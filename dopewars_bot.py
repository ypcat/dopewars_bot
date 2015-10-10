#!/usr/bin/env python

# TODO reply markup

import codecs
import os
import sys
import traceback

import telegram
import dopewars

def main():
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    sys.stderr = codecs.getwriter('utf8')(sys.stderr)
    token_file = os.path.join(os.path.dirname(__file__), 'token')
    bot = telegram.Bot(open(token_file).read().strip())
    update_id = 0
    while True:
        try:
            for update in bot.getUpdates(offset=update_id+1, timeout=60):
                update_id = update.update_id
                chat_id = update.message.chat_id
                text = update.message.text
                name = update.message.from_user.name
                print name, chat_id, text
                messages = dopewars.play(chat_id, text.split('@')[0])
                if messages:
                    text = '\n'.join(messages)
                    print text
                    bot.sendMessage(chat_id=chat_id, text=text)
        except:
            traceback.print_exc()

if __name__ == '__main__':
    main()
