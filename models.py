# -*- coding: utf-8 -*-

from peewee import (Model, CharField, SqliteDatabase, IntegerField, ForeignKeyField,
                    OperationalError)
from playhouse.fields import ManyToManyField

db = SqliteDatabase('instagram.db')


class User(Model):
    username = CharField()
    bio = CharField()
    website = CharField()
    profile_picture = CharField()
    full_name = CharField()
    user_id = CharField()

    class Meta:
        database = db


class Media(Model):
    user = ManyToManyField(User, related_name='medias')

    class Meta:
        database = db


class Stat(Model):
    followed_by = IntegerField()
    follows = IntegerField()
    media = ForeignKeyField(rel_model=Media)

    class Meta:
        database = db


def create_database():
    db.connect()
    try:
        db.create_tables((User, Stat, Media))
    except OperationalError:
        print 'database already exists'
