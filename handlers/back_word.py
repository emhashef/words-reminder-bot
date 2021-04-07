from telegram.ext import CallbackContext, CallbackQueryHandler, Updater
from utils.decorators import have_access
from utils.dictionary import get_def_markdown
from database import User, Word


@have_access
def back_word(updater: Updater, context: CallbackContext, user: User):
    query = updater.callback_query
    word_id = query.data.split()[1]
    word = Word.get_or_none(id=word_id)

    if not word:
        query.answer(text="word not found")
        return

    word.back_to_first_level()
    user.answered()
    query.answer(text="success")

    query.edit_message_caption(caption="Read the definition again. 💪\n\n" +
                               get_def_markdown(word.value), parse_mode="Markdown")


handler = CallbackQueryHandler(back_word, pattern="back")
