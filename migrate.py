import importlib
from database import User
from app import config
from database import *
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def migrate():
    database_module = importlib.import_module('database')
    for model in database_module.__all__:
        database_module.__dict__[model].create_table()
    
    logger.info('tables migrated successfuly')

def seed_words(user):
    c = 0
    with open('assets/words.txt','r') as f:
        for word in f:
            word = word.strip()
            if word:
                Word.create(
                    user=user,
                    value=word
                )
                c +=1
    logger.info(str(c) + ' words seeded successfully')

def seed():
    user = User.create(
        username=config('username')
    )
    logger.info('user seeded successfully')
    seed_words(user)

if __name__ == '__main__':
    migrate()
    seed()
