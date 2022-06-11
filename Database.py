import Config
from pathlib import Path
from peewee import SqliteDatabase, Model, AutoField, TextField, BlobField

db = SqliteDatabase(Config.DATABASE_FILENAME)
exists = Path(Config.DATABASE_FILENAME).exists()


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = AutoField(column_name="user_id")
    name = TextField(column_name="name")
    surname = TextField(column_name="surname")
    email = TextField(column_name="email", unique=True)
    eth_address = TextField(column_name="eth_address", unique=True)
    password = BlobField(column_name="password")
    auth_token = TextField(column_name="auth_token")

    class Meta:
        table_name = "Users"


if not exists:
    User.create_table()
