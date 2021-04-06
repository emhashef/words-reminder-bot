from telegram.ext import Updater, CallbackContext, CommandHandler,ConversationHandler,MessageHandler,Filters
from database import User
from utils.decorators import have_access
from datetime import datetime, timedelta

ANSWER = 1

@have_access
def ask(update: Updater, context: CallbackContext,user: User):
    update.effective_user.send_message('how many hours?')
    return ANSWER

@have_access
def snooze(update: Updater, context: CallbackContext, user: User):
    hour = update.effective_message.text
    if not hour.isnumeric():
        update.effective_user.send_message('add hour for snooze in command')
        return

    user.ready_at = datetime.now() + timedelta(hours=int(hour))
    user.save()

    update.effective_user.send_message(f'you snoozed for {hour} hour to retrieve any word')


handler =  ConversationHandler(
    entry_points=[CommandHandler('snooze', ask)],
    states={
        ANSWER: [MessageHandler(Filters.text,snooze)]
    },
    fallbacks=[]
)
