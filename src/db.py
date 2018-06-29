from peewee import SqliteDatabase, Model, IntegerField, BooleanField

db = SqliteDatabase('../db/ifi_blog_chats.db')


def create_tables():
    with db:
        db.create_tables([Chat])


class Chat(Model):
    chat_id = IntegerField()
    subscribed = BooleanField(default=True)

    class Meta:
        database = db
