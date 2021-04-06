from telegram.ext import Updater, CallbackContext, CommandHandler,ConversationHandler,Filters,MessageHandler
from database import User
from utils.decorators import have_access
from datetime import datetime, timedelta


ANSWER = 1

@have_access
def ask(update: Updater, context: CallbackContext,user: User):
    update.effective_user.send_message('how many hours?')
    return ANSWER

@have_access
def snooze_news(update: Updater, context: CallbackContext, user: User):
    hour = update.effective_message.text
    if not hour.isnumeric():
        update.effective_user.send_message('hour must be numeric')
        return

    user.ready_for_news_at = datetime.now() + timedelta(hours=int(hour))
    user.new_words = 0
    user.save()

    update.effective_user.send_message(f'you snoozed for {hour} hour to retrieve new words')


handler = ConversationHandler(
    entry_points=[CommandHandler('snooze_news', ask)],
    states={
        ANSWER: [MessageHandler(Filters.text,snooze_news)]
    },
    fallbacks=[]
)