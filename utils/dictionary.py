

def get_def_url(word: str):
    return f'https://www.oxfordlearnersdictionaries.com/us/definition/english/{word.lower()}'

def get_def_markdown(word: str):
    return f'[english definition]({get_def_url(word)})'