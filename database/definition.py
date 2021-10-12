from peewee import TextField, CharField, BooleanField, DateTimeField, BigIntegerField, IntegerField
from database.base import BaseModel
from datetime import datetime, timedelta


class Definition(BaseModel):
    word= CharField()
    definition=TextField(null=True)