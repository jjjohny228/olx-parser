from datetime import datetime
from peewee import (Model, SqliteDatabase, BigIntegerField, IntegerField, DateTimeField, CharField,
                    BooleanField, FloatField, ForeignKeyField)

db = SqliteDatabase('database.db')


class _BaseModel(Model):
    class Meta:
        database = db


class User(_BaseModel):
    """
    The model contains users information.
    """
    class Meta:
        db_table = 'users'

    username = CharField(default='Пользователь')
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    telegram_id = BigIntegerField(unique=True, null=False)
    registration_timestamp = DateTimeField(default=datetime.now())
    admin = BooleanField(default=False)


class Plan(_BaseModel):
    """
    The model contains available plans
    """
    class Meta:
        db_table = 'plans'

    name = CharField()
    price = FloatField()
    max_targets = IntegerField()


class Subscription(_BaseModel):
    """
    The model contains users subscriptions.
    """
    class Meta:
        db_table = 'subscriptions'

    user = ForeignKeyField(User, backref='subscriptions')
    plan = ForeignKeyField(Plan, backref='subscriptions')
    started_at = DateTimeField(default=datetime.now())
    trial_end_at = DateTimeField()


class Target(_BaseModel):
    """
    The model contains user targets.
    A target is a URL with filters that will be parsed by the program
    """
    class Meta:
        db_table = 'targets'

    user = ForeignKeyField(User, backref='targets')
    name = CharField()
    url = CharField()
    chat_id = CharField()
    active = BooleanField(default=True)


def register_models() -> None:
    for model in _BaseModel.__subclasses__():
        model.create_table()
