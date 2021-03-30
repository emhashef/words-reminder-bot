from database import Word, User
from datetime import datetime,timedelta
from app import bot
from utils.image import generate_image
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import time
from logging import getLogger

logger = getLogger(__name__)


def remind():
    for user in User.select():
        if user.ready and not user.reminded:
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

            url = f"[definition](https://www.oxfordlearnersdictionaries.com/us/definition/english/{word.value.lower()})"

            if word.level == 0:
                caption = "Read this word or delete this word if its known.\n\n" + url
                replay_markup = [
                    [InlineKeyboardButton("Next", callback_data="next " + str(word.id)),
                     InlineKeyboardButton("Delete", callback_data="delete " + str(word.id))]
                ]
            else:
                caption = "Do you rememeber this word?"
                replay_markup = [
                    [InlineKeyboardButton("Yes", callback_data="next "+str(word.id)),
                     InlineKeyboardButton('No', callback_data='back ' + str(word.id))]
                ]

            if word.level == 0 and not user.ready_for_news:
                return

            message = bot.send_photo(chat_id=user.chat_id, photo=generate_image(
                word.value), caption=caption, reply_markup=InlineKeyboardMarkup(replay_markup), parse_mode="Markdown")

            user.set_last_remind(message.message_id, datetime.now())

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
        time.sleep(30)
