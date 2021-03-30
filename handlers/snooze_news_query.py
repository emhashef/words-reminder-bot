from utils.decorators import have_access
from snooze_news import snooze_news
from telegram.ext import CallbackQueryHandler

@have_access
def snooze_news_query(update,context,user):
    query = update.callback_query
    hour = query.split()[1]
    if not hour and hour.isnumeric():
        return

    user.ready_for_news_at = datetime.now() + timedelta(hours=int(hour))
    user.new_words = 0
    user.save()
    query.answer(text=f'snoozed for {hour} hour')

handler = CallbackQueryHandler(snooze_news_query,pattern='snooze_news')