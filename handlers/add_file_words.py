from telegram.ext import Updater, CallbackContext, CommandHandler,ConversationHandler,MessageHandler,Filters
from telegram.ext.filters import Filters
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from database import User, Word
from utils.decorators import have_access
from utils.image import generate_image
import io, codecs


@have_access
def add_file_word(update: Updater, context: CallbackContext, user: User):
    document = update.effective_message.document
    
    if document.mime_type != 'text/plain':
        return update.effective_user.send_message('send text file !')

    out = update.effective_message.document.get_file().download_as_bytearray()

    for word in out.decode('utf-8').split('\n'):
        word = word.strip()

        if not word:
            continue

        Word.create(
                user=user,
                value=word
            )

    update.effective_user.send_message('Your words added successfully. It will be reminded repetitively ⌛')


handler = MessageHandler(Filters.document, add_file_word)