

def get_def_url(word: str):
    return f't.me/iv?url=https://abadis.ir/entofa/{word.lower()}&rhash=c2171b285298d6'

def get_def_markdown(word: str):
    return f'[definition]({get_def_url(word)})'