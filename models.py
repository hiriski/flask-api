import datetime
from peewee import *

sqliteDatatabase = SqliteDatabase('new_datatabase.db')

class BaseModel(Model):
    class Meta:
        database = sqliteDatatabase

class User(BaseModel):
    username    = CharField(unique=True, max_length=25)
    password    = CharField()

class Blog(BaseModel):
    user_id     = ForeignKeyField(User, backref="daftarBlog")
    title       = CharField(null=False)
    content     = TextField()
    publish_at  = DateTimeField(default=datetime.datetime.now)

# Simpan di dalam sebuah function biar gampang panggilnya
def initialize():
    sqliteDatatabase.connect()
    # Create tables
    sqliteDatatabase.create_tables([Blog, User], safe=True)
    # Jangan lupa close setelah migration
    sqliteDatatabase.close()