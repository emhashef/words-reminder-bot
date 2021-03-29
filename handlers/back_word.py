from telegram.ext import CallbackContext, CallbackQueryHandler,Updater
from utils.decorators import have_access
from database import User,Word

@have_access
def back_word(updater: Updater, context: CallbackContext, user:User):
    query = updater.callback_query
    word_id = query.data.split()[1]
    word = Word.get_or_none(id=word_id)

    if not word:
        query.answer(text="word not found")
        return

    word.back_to_first_level()
    user.set_ready()
    query.answer(text="success")
    url = f"[definition](https://www.oxfordlearnersdictionaries.com/us/definition/english/{word.value.lower()})"

    query.edit_message_caption(caption="Read the definition again. 💪\n\n" + url,parse_mode="Markdown")

handler = CallbackQueryHandler(back_word, pattern="back")