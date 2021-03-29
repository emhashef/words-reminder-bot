from .base import BaseModel
from peewee import CharField, DateTimeField, SmallIntegerField, ForeignKeyField
from .user import User
from datetime import datetime, timedelta


class Word(BaseModel):
    user = ForeignKeyField(User, backref='words')
    value = CharField()
    remind_at = DateTimeField(null=True)
    level = SmallIntegerField(default=0)

    def go_next_level(self):
        if self.level == 0:
            self.remind_at = datetime.now() + timedelta(days=1)
        elif self.level == 1:
            self.remind_at = datetime.now() + timedelta(days=2)
        elif self.level == 2:
            self.remind_at = datetime.now() + timedelta(days=4)
        elif self.level == 3:
            self.remind_at = datetime.now() + timedelta(days=8)
        elif self.level == 4:
            self.remind_at = datetime.now() + timedelta(days=16)
        elif self.level == 5:
            return self.delete_instance()

        self.level += 1
        return self.save()

    def back_to_first_level(self):
        self.level = 1
        self.remind_at = self.remind_at = datetime.now() + timedelta(days=1)
        self.save()


