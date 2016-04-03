# -*- coding: utf-8 -*-

from peewee import Model, CharField, SqliteDatabase, IntegerField, ForeignKeyField
from playhouse.fields import ManyToManyField

DB_FILENAME = 'instagram.db'

db = SqliteDatabase(DB_FILENAME)


class Stat(Model):
    followed_by = IntegerField()
    follows = IntegerField()
    media = IntegerField()

    class Meta:
        database = db


class User(Model):
    username = CharField()
    bio = CharField()
    website = CharField()
    profile_picture = CharField()
    full_name = CharField()
    user_id = CharField()
    stat = ForeignKeyField(Stat)

    class Meta:
        database = db


class Media(Model):
    users = ManyToManyField(User, related_name='medias')
    media_id = CharField()

    class Meta:
        database = db
