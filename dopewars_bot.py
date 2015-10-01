#!/usr/bin/env python

import telegram

from dopewars import start, is_finish, get_message, process

def main():
    token = open('token').read()
    bot = telegram.Bot(token)
    update_id = 0
    sessions = {}
    while True:
        for update in bot.getUpdates(offset=update_id, timeout=60):
            try:
                update_id = update.update_id + 1
                chat_id = update.message.chat_id
                input = update.message.text.encode('utf8')
                name = update.message.from_user.name
                text = ''
                print name, input
                if input == 'start':
                    id = start(name)
                    sessions[chat_id] = id
                    print "start new game, chat id %s, game id %d" % (chat_id, id)
                    text = get_message(id)
                elif chat_id in sessions and not is_finish(id):
                    id = sessions[chat_id]
                    if process(id, input):
                        text = get_message(id)
                if text:
                    print text
                    bot.sendMessage(chat_id=chat_id, text=text)
            except:
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    main()

