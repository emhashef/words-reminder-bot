from utils.decorators import have_access
from snooze_news import snooze_news
from telegram.ext import CallbackQueryHandler

@have_access
def snooze_news_query(update,context,user):
    context.args = [updater.callback_query.data.split()[1]]
    snooze_news(update,context,user)

handler = CallbackQueryHandler(snooze_news_query,pattern='snooze_news')