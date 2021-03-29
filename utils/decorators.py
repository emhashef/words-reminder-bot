from telegram.ext import Updater, CallbackContext
from database import User


def have_access(handler):
    def wrapper(update: Updater, context: CallbackContext):
        user = User.get_or_none(username=update.effective_user.username)
        if not user:
            update.effective_user.send_message(
                "You don't have access to use this bot")
            return

        return handler(update, context, user)
    return wrapper
