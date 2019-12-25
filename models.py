import datetime
from peewee import *

db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

class Blog(BaseModel):
    title = CharField(null=False)
    content = TextField()
    create_at = DateTimeField(default=datetime.datetime.now)

class Message(BaseModel):
    content = TextField()
    create_at = DateTimeField(default=datetime.datetime.now)

# Simpan di dalam sebuah function biar gampang panggilnya
def initialize():
    db.connect()

    db.create_tables([Blog, Message], safe=True)

    # Jangan lupa close setelah migration
    db.close()