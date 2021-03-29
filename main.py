from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from app import config, updater
import logging
from utils.decorators import have_access
from utils.image import generate_image
from jobs.remind import remind
import importlib
import handlers
import time
import os

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


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


PORT = int(os.environ.get('PORT', 5000))

updater.start_webhook(listen="0.0.0.0",
                      port=int(PORT),
                      url_path=config('token'))
updater.bot.setWebhook(config('url') + config('token'))

updater.start_polling()
updater.idle()
