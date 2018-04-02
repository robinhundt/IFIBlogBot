from inspect import getmembers, isfunction

from telegram import ext

import config
import handlers
from ifi_feed import Feed

latestEntry = None


def check_for_new_entry(bot, job):
    global latestEntry
    feed = Feed(config.feed['url'])
    feed.update()
    latest = feed.latest_entry()
    if latestEntry is None or latestEntry < latest:
        latestEntry = latest
        bot.send_message(chat_id='342310826', parse_mode='Markdown', text=str(latest))


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
    IFI_bot = IFIBot()
    handler_funcs = getmembers(handlers, isfunction)
    IFI_bot.init_command_handlers(handler_funcs)
    IFI_bot.start_bot()
