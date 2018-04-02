import config
from ifi_feed import Feed


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown',
                     text="*Hey!* From now on you'll receive the latest IFI-Blog"
                          "posts directly here!")


def about(bot, update):
    bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown',
                     text="Hey! I'm a small bot written by @robinhundt that serves you the"
                          "newest updates from the blog of the cs deanery in Goettingen.")


def blog(bot, update):
    bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown',
                     text="The blog of the cs deanery can be read "
                          "[here](blog.stud.uni-goettingen.de/informatikstudiendekanat/).")


def blog_latest(bot, update):
    feed = Feed(config.feed['url'])
    feed.update()
    bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown',
                     text=str(feed.latest_entry()))

