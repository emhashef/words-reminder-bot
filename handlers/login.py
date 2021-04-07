from telegram.ext import Updater, CommandHandler, CallbackContext
from database.user import User


def login(update: Updater, context: CallbackContext):

    user,_ = User.get_or_create(username=update.effective_user.username)

    if not user:
        update.effective_user.send_message("You don't have access to use this bot")
        return
    
    user.name = update.effective_user.full_name
    user.username = update.effective_user.username
    user.chat_id = update.effective_user.id
    user.save()
    update.effective_user.send_message("You are registered, now you can use it.")

handler = CommandHandler(
    'start',
    login
)