from telegram.ext import Updater, CallbackContext, CommandHandler,ConversationHandler,MessageHandler,Filters
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from database import User, Word
from utils.decorators import have_access
from utils.image import generate_image

ANSWER = 1

@have_access
def ask(update: Updater, context: CallbackContext,user: User):
    update.effective_user.send_message('enter your word:')
    return ANSWER

@have_access
def add_word(update: Updater, context: CallbackContext, user: User):

    word = Word(
        user=user,
        value=update.effective_message.text
    )
    # word.go_next_level()
    # url = f"[definition](https://www.oxfordlearnersdictionaries.com/us/definition/english/{word.value.lower()})"
    # caption = "Read this word or delete this word if its known.\n\n" + url
    # replay_markup = [
    #     [InlineKeyboardButton("Next", callback_data="next " + str(word.id)),InlineKeyboardButton("Delete", callback_data="delete " + str(word.id))]
    # ]
    # word.set_reminded()

    # update.effective_user.send_photo(photo=generate_image(word.value),caption=caption, reply_markup=InlineKeyboardMarkup(replay_markup),parse_mode="Markdown")

    update.effective_user.send_message('Your word added successfully ✅.\nIt will be reminded repetitively.⌛')
    return ConversationHandler.END

handler = ConversationHandler(
    entry_points=[CommandHandler('add', ask)],
    states={
        ANSWER: [MessageHandler(Filters.text,add_word)]
    },
    fallbacks=[]
)
