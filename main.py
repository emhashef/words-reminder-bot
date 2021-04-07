from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from app import config, updater
import logging
from utils.decorators import have_access
from utils.image import generate_image
from jobs.remind import remind
from database import User
import importlib
import handlers
import time
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def error_handler(update: object, context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    user = User.where(username=config('username')).get_or_none()
    
    if user and user.chat_id:
        # Finally, send the message
        context.bot.send_message(chat_id=user.chat_id, text=message, parse_mode='HTML')

@have_access
def hello(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.effective_user.send_message('pass argument')
        return

    photo = generate_image(context.args[0])
    update.effective_user.send_photo(photo)


updater.dispatcher.add_handler(CommandHandler('hello', hello))
for handler_name in handlers.__all__:
    handler_module = importlib.import_module('handlers.'+handler_name)
    handler = getattr(handler_module, 'handler', None)
    if handler:
        updater.dispatcher.add_handler(handler)

updater.dispatcher.add_error_handler(error_handler)

PORT = int(config('PORT', 5000))

if config('environment') == 'dev':
    updater.start_polling()
else:
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=config('token'))
    updater.bot.setWebhook(config('url') + config('token'))


updater.idle()
