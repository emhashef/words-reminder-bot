import requests
from bs4 import BeautifulSoup
from database.definition import Definition

def get_def_from_db(word: str):
    definition = Definition.select().where(Definition.word == word).first()
    return definition.definition if definition else None

def get_def_url(word: str):
    return f'https://www.oxfordlearnersdictionaries.com/us/definition/english/{word.lower()}'

def get_def_markdown(word: str):

    db_def = get_def_from_db(word.lower())
    if( db_def is None):
        try:

            res = requests.get(f'https://abadis.ir/entofa/{word.lower()}')
            soup = BeautifulSoup(res.content, 'html.parser')
            translate = soup.select('.boxMain')[0].contents[3].replace(':','').strip()
            Definition.create(word=word.lower(),definition=translate)
        except Exception:
            translate = ''
    else:
        translate = db_def
    
    return translate +  '\n\n' + f'[definition]({get_def_url(word)})'
