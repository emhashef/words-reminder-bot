from peewee import TextField, CharField, BooleanField, DateTimeField, BigIntegerField, IntegerField
from database.base import BaseModel
from datetime import datetime, timedelta
from jobs.remind import remind


class User(BaseModel):
    name = CharField(null=True)
    chat_id = CharField(null=True)
    username = CharField()
    ready_at = DateTimeField(default=datetime.now, null=True)
    ready_for_news_at = DateTimeField(default=datetime.now, null=True)
    last_remind_id = BigIntegerField(null=True)
    last_remind_at = DateTimeField(null=True)
    last_remind_alert = BooleanField(default=False)
    reminded = BooleanField(default=False)
    new_words = IntegerField(default=0)

    def set_ready(self):
        self.ready = datetime.now()
        self.save()

    def set_unready(self, until=None):
        self.ready_at = datetime.now() + until or timedelta()
        self.save()

    def set_last_remind(self, id=None, time=None):
        self.last_remind_id = id
        self.last_remind_at = time
        self.reminded = True
        self.save()

    @property
    def ready(self):
        return self.ready_at < datetime.now()

    @property
    def ready_for_news(self):
        return self.ready_for_news_at < datetime.now()

    
    def set_reminded(self):
        self.reminded = True
        self.save()
    
    def set_unreminded(self):
        self.reminded = False
        self.save()

    def answered(self):
        self.last_remind_alert = False
        self.reminded = False
        self.save()
        remind()
