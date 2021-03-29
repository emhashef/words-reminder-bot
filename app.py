from peewee import SqliteDatabase,PostgresqlDatabase
import yaml
from telegram.ext import Updater
import os

config_filename = 'config.yml'


def config(key: str, default=None):
    stream = open(config_filename, 'r')
    config = yaml.load(stream, Loader=yaml.FullLoader)

    current_value = config
    for current_key in key.split('.'):
        current_value = current_value.get(current_key)

    return default if not current_value else current_value


# db = SqliteDatabase(config('db', 'database.sqlite'))
db = PostgresqlDatabase(os.environ.get('DATABASE_URL'))

updater = Updater(config('token'))

bot = updater.bot