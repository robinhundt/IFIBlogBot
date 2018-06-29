import config
from src.ifi_feed import Feed
from src.db import Chat, db


def start(bot, update):
    with db:
        chat, created = Chat.get_or_create(chat_id=update.message.chat_id)
        chat.subscribed = True
        chat.save()
        bot.send_message(chat_id=chat.chat_id, parse_mode='Markdown',
                         text="*Hey!* From now on you'll receive the latest IFI-Blog"
                              "posts directly here!")


def stop(bot, update):
    with db:
        chat, created = Chat.get_or_create(chat_id=update.message.chat_id)
        chat.subscribed = False
        chat.save()
        if created:
            bot.send_message(chat_id=chat.chat_id, parse_mode='Markdown',
                             text="Since you weren't subscribed in the first place, "
                                  "you'll receive no automatic messages.")
        else:
            bot.send_message(chat_id=chat.chat_id, parse_mode='Markdown',
                             text="You'll receive no more automatic blog updates.")


def about(bot, update):
    bot.send_message(chat_id=update.message.chat_id, parse_mode='Markdown',
                     text="Hey! I'm a small bot written by @robinhundt that serves you the "
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

