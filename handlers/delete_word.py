from telegram.ext import Updater, CallbackContext, CallbackQueryHandler
from database import Word, User
from utils.decorators import have_access


@have_access
def delete_word(updater: Updater, context: CallbackContext, user: User):
    query = updater.callback_query
    word_id = query.data.split()[1]
    word = Word.get_or_none(id=word_id)

    if not word:
        query.answer(text='word not found')
        return

    word.delete_instance()
    query.answer(text="word deleted")

    # if user.last_remind_id == query.message.message_id:
    user.answered()

    query.edit_message_caption(updater.effective_message.caption_markdown + ' ❌', parse_mode="Markdown")


handler = CallbackQueryHandler(delete_word, pattern='delete')
