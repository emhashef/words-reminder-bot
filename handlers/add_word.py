from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from database import User, Word
from utils.decorators import have_access
from utils.image import generate_image


@have_access
def add_word(update: Updater, context: CallbackContext, user: User):
    if not context.args:
        update.effective_user.send_message('pass word argument')
        return

    word = Word(
        user=user,
        value=" ".join(context.args)
    )
    word.go_next_level()
    url = f"[definition](https://www.oxfordlearnersdictionaries.com/us/definition/english/{word.value.lower()})"
    caption = "Read this word or delete this word if its known.\n\n" + url
    replay_markup = [
        [InlineKeyboardButton("Delete", callback_data="delete " + str(word.id))]
    ]

    update.effective_user.send_photo(photo=generate_image(word.value),caption=caption, reply_markup=InlineKeyboardMarkup(replay_markup),parse_mode="Markdown")


handler = CommandHandler('add', add_word)
