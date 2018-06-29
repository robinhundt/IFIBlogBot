from datetime import datetime

from peewee import SqliteDatabase, Model, IntegerField, BooleanField, DateTimeField

db = SqliteDatabase('/db/ifi_blog_chats.db')


def create_tables():
    with db:
        db.create_tables([Chat])


class Chat(Model):
    chat_id = IntegerField()
    subscribed = BooleanField(default=True)
    datetime_last_received_entry = DateTimeField(default=datetime.now())

    class Meta:
        database = db
