from inspect import getmembers, isfunction
import os

from telegram import ext

from settings import conf
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
        feed = Feed(conf.feed['url'])
        feed.update()
        latest = feed.latest_entry()
        with db:
            self.latest_entry = latest
            subscribed_chats = Chat.select().where(Chat.subscribed)
            for chat in subscribed_chats:
                if chat.datetime_last_received_entry < latest.published:
                    bot.send_message(chat_id=chat.chat_id, parse_mode='Markdown', text=str(latest))
                    chat.datetime_last_received_entry = latest.published
                    chat.save()


if __name__ == '__main__':
    bot_token = os.environ['BOT_TOKEN']
    create_tables()
    IFI_bot = IFIBot(token=bot_token)
    handler_funcs = getmembers(handlers, isfunction)
    IFI_bot.init_command_handlers(handler_funcs)
    IFI_bot.start_bot()
