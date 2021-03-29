import importlib
from database import User
from app import config
from database import *





def migrate():
    database_module = importlib.import_module('database')
    for model in database_module.__all__:
        database_module.__dict__[model].create_table()


def seed():
    User.create(
        username=config('username')
    )


if __name__ == '__main__':
    migrate()
    seed()
