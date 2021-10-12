from peewee import SqliteDatabase, PostgresqlDatabase, Proxy
from telegram.ext import Updater, Dispatcher, JobQueue
from telegram import Bot
from queue import Queue
import os
from playhouse.db_url import connect
import dotenv

dotenv.load_dotenv()

def config(key: str, default=None):
    return os.environ.get(key) or os.environ.get(key.upper()) or default


# db = SqliteDatabase(config('db', 'database.sqlite'))
db = Proxy()
db.initialize(connect(config('DATABASE_URL', 'sqlite:///database.sqlite')))

class CustomDispatcher(Dispatcher):
    def process_update(self, update):
        with db.atomic() as txn:
            super().process_update(update)
        db.close()


updater = Updater(dispatcher=CustomDispatcher(Bot(config('token')), Queue(), job_queue=JobQueue()),workers=None)

bot = updater.bot
