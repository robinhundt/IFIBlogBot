import feedparser
import html

from dateutil import parser


class Entry:
    def __init__(self, entry_dict):
        self.title = entry_dict['title']
        self.link = entry_dict['link']
        self.summary = entry_dict['summary']
        self.published = parser.parse(entry_dict['published'])

    def __eq__(self, other):
        return self.published == other.published

    def __lt__(self, other):
        return self.published < other.published

    def __str__(self):
        return f"*{self.title}*\n" \
               f"{self.summary}\n" \
               f"{self.link}"


class Feed:
    def __init__(self, feed_url):
        self.feed_url = feed_url
        self.feed = {}
        self.title = ''
        self.link = ''
        self.entries = []
        self.updated = None

    def update(self):
        parsed_feed = feedparser.parse(self.feed_url)
        self.feed = parsed_feed
        self.title = self.feed['feed']['title']
        self.link = self.feed['feed']['link']
        self.updated = self.feed['feed']['updated']
        self.entries = sorted([Entry(entry) for entry in self.feed['entries']], reverse=True)

    def latest_entry(self):
        return html.unescape(self.entries[0])
