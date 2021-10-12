

def get_def_url(word: str):
    return f'https://abadis.ir/entofa/{word.lower()}'

def get_def_markdown(word: str):
    return f'[definition]({get_def_url(word)})'