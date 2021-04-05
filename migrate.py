import importlib
from database import User
from app import config,db
from database import *
import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

should_refresh = ('-r' or '--refresh') in sys.argv
should_seed = ('-s' or '--seed') in sys.argv


def migrate():
    database_module = importlib.import_module('database')
    if should_refresh:
        db.drop_tables([database_module.__dict__[table] for table in reversed(database_module.__all__)])
    db.create_tables([database_module.__dict__[table] for table in database_module.__all__])
    
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
    if should_seed:
        seed()
