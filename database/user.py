from peewee import TextField, CharField, BooleanField
from database.base import BaseModel


class User(BaseModel):
    name = CharField(null=True)
    chat_id = CharField(null=True)
    username = CharField()
    ready = BooleanField(default=True)

    def set_ready(self):
        self.ready = True
        self.save()

    def set_unready(self):
        self.ready = False
        self.save()
