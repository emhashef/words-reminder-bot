from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
from utils.decorators import have_access
from database import User, Word


@have_access
def next_word(updater: Updater, context: CallbackContext, user: User):
    query = updater.callback_query
    word_id = query.data.split()[1]
    word = Word.get_or_none(id=word_id)

    if not word:
        query.answer(text="word not found")
        return

    word.go_next_level()
    user.set_ready()
    query.answer(text="success")

    query.edit_message_caption(updater.message.caption)


handler = CallbackQueryHandler(next_word, pattern='next')
