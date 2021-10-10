from database import Word, User
from datetime import datetime,timedelta
from app import bot, db
from utils.image import generate_image
from utils.dictionary import get_def_markdown
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import Unauthorized
import time
from logging import getLogger

logger = getLogger(__name__)

def remind_user(user):
    word = (user.words
        .where((Word.remind_at < datetime.now()) | (Word.remind_at == None))
        .order_by(Word.remind_at.desc())
        .order_by(Word.id.asc())
        .limit(1)
        .first())

    if not word:
        logger.info(
            'there is no word to remind to user: ' + user.username)
        return

    if word.level == 0:
        caption = "Read this word or delete this word if its known.\n\n" + get_def_markdown(word.value)
        replay_markup = [
            [InlineKeyboardButton("Next", callback_data="next " + str(word.id)),
                InlineKeyboardButton("Delete", callback_data="delete " + str(word.id))]
        ]
        user.new_words += 1

        if user.new_words > 10:
            caption += '\n\n(you can snooze new words !)'
            replay_markup.append(
                [InlineKeyboardButton("Snooze New Words (24h)",callback_data="snooze_news 24")]
            )
    else:
        caption = "Do you rememeber this word?"
        replay_markup = [
            [InlineKeyboardButton("Yes", callback_data="next "+str(word.id)),
                InlineKeyboardButton('No', callback_data='back ' + str(word.id))]
        ]

    if word.level == 0 and not user.ready_for_news:
        return
        
    try:
        message = bot.send_photo(chat_id=user.chat_id, photo=generate_image(
            word.value), caption=caption, reply_markup=InlineKeyboardMarkup(replay_markup), parse_mode="Markdown")
        
        user.last_remind_id = message.message_id
        user.last_remind_at = datetime.now()
        user.reminded = True
    
    except Unauthorized:
        user.chat_id = None

    user.save()


def remind():
    for user in User.select().where(User.chat_id.is_null(False)):
        if user.ready and not user.reminded:
            
            remind_user(user)

        elif user.ready and user.reminded and not user.last_remind_alert:
            if user.last_remind_at < datetime.now() - timedelta(hours=1):
                bot.send_message(chat_id=user.chat_id, text="don't forget to answer this word !",
                                reply_to_message_id=user.last_remind_id)
                user.last_remind_alert = True
                user.save()
        else:
            logger.info(f'user: {user.username} is unready to remind')


def start_reminding():
    logger.info('start reminding...')
    while True:
        
        remind()
        db.close()
        
        time.sleep(5)
