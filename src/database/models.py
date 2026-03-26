from datetime import datetime
from peewee import Model, SqliteDatabase, BigIntegerField, DateTimeField, CharField, BooleanField, ForeignKeyField

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
    language_code = CharField(default='ru')


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


class Advertisement(_BaseModel):
    """
    The models contain all advertisements that were found
    """
    target = ForeignKeyField(Target, backref='advertisements')
    url = CharField(unique=True)



def register_models() -> None:
    db.connect(reuse_if_open=True)
    for model in _BaseModel.__subclasses__():
        model.create_table(safe=True)

    user_columns = {column.name for column in db.get_columns(User._meta.table_name)}
    if 'language_code' not in user_columns:
        db.execute_sql("ALTER TABLE users ADD COLUMN language_code VARCHAR(8) DEFAULT 'ru'")
