from telegram.ext import Updater, CallbackContext, CommandHandler
from database import User
from utils.decorators import have_access
from datetime import datetime, timedelta


@have_access
def snooze(update: Updater, context: CallbackContext, user: User):
    hour = ''.join(context.args).strip()
    if not hour and not hour.isnumeric():
        update.effective_user.send_message('add hour for snooze in command')
        return

    user.ready_at = datetime.now() + timedelta(hours=int(hour))
    user.save()

    update.effective_user.send_message(f'you snoozed for {hour} hour to retrieve any word')


handler = CommandHandler('snooze', snooze)
