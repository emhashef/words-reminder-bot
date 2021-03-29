from peewee import SqliteDatabase, PostgresqlDatabase, Proxy
from telegram.ext import Updater
import os
from playhouse.db_url import connect
import dotenv

dotenv.load_dotenv()

def config(key: str, default=None):
    return os.environ.get(key) or os.environ.get(key.upper()) or default


# db = SqliteDatabase(config('db', 'database.sqlite'))
db = Proxy()
db.initialize(connect(config('DATABASE_URL', 'sqlite:///database.sqlite')))

updater = Updater(config('token'))

bot = updater.bot
