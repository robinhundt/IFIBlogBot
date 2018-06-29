from inspect import getmembers, isfunction

from telegram import ext

import config
from src import handlers
from src.ifi_feed import Feed
from src.db import db, Chat, create_tables


class IFIBot:
    def __init__(self, token):
        self.token = token
        self.updater = ext.Updater(token=token)
        self.dispatcher = self.updater.dispatcher
        self.job_queue = self.updater.job_queue
        self.command_handlers = {}

        self.latest_entry = None

    def init_command_handlers(self, cmd_funcs):
        for cmd_func in cmd_funcs:
            handler = ext.CommandHandler(cmd_func[0], cmd_func[1])
            self.command_handlers[cmd_func[0]+'_handler'] = handler
            self.dispatcher.add_handler(handler)

    def start_bot(self):
        self.updater.start_polling()
        self.job_queue.run_repeating(self._check_for_new_entry, interval=1800)

    def stop_bot(self):
        self.updater.stop()

    def _check_for_new_entry(self, bot, job):
        feed = Feed(config.feed['url'])
        feed.update()
        latest = feed.latest_entry()
        if self.latest_entry is None or self.latest_entry < latest:
            with db:
                self.latest_entry = latest
                subscribed_chats = Chat.select().where(Chat.subscribed)
                for chat in subscribed_chats:
                    bot.send_message(chat_id=chat.chat_id, parse_mode='Markdown', text=str(latest))


if __name__ == '__main__':
    with open('../token') as f:
        bot_token = f.readline().strip()
    create_tables()
    IFI_bot = IFIBot(token=bot_token)
    handler_funcs = getmembers(handlers, isfunction)
    IFI_bot.init_command_handlers(handler_funcs)
    IFI_bot.start_bot()
