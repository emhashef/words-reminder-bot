from utils.decorators import have_access
from telegram.ext import CallbackQueryHandler
from datetime import datetime,timedelta

@have_access
def snooze_news_query(update,context,user):
    query = update.callback_query
    hour = query.data.split()[1]
    if not hour and hour.isnumeric():
        return

    user.ready_for_news_at = datetime.now() + timedelta(hours=int(hour))
    user.new_words = 0
    user.save()
    query.answer()
    update.effective_user.send_message(f'you snoozed for {hour} hour to retrieve new words')

handler = CallbackQueryHandler(snooze_news_query,pattern='snooze_news')