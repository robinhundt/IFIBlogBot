from inspect import getmembers, isfunction

from telegram import ext

import config
import handlers
from ifi_feed import Feed
from db import db, Chat

latestEntry = None


def check_for_new_entry(bot, job):
    global latestEntry
    feed = Feed(config.feed['url'])
    feed.update()
    latest = feed.latest_entry()
    with db:
        subscribed_chats = Chat.select().where(Chat.subscribed)
        if latestEntry is None or latestEntry < latest:
            latestEntry = latest
            for chat in subscribed_chats:
                bot.send_message(chat_id=chat.chat_id, parse_mode='Markdown', text=str(latest))


class IFIBot:
    def __init__(self, token):
        self.token = token
        self.updater = ext.Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue
        self.command_handlers = {}

    def init_command_handlers(self, cmd_funcs):
        for cmd_func in cmd_funcs:
            handler = ext.CommandHandler(cmd_func[0], cmd_func[1])
            self.command_handlers[cmd_func[0]+'_handler'] = handler
            self.dispatcher.add_handler(handler)

    def start_bot(self):
        self.updater.start_polling()
        self.job_queue.run_repeating(check_for_new_entry, interval=10)

    def stop_bot(self):
        self.updater.stop()


if __name__ == '__main__':
    with open('token') as f:
        bot_token = f.readline().strip()
        IFI_bot = IFIBot(token=bot_token)
        handler_funcs = getmembers(handlers, isfunction)
        IFI_bot.init_command_handlers(handler_funcs)
        IFI_bot.start_bot()
