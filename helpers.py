# -*- coding: utf-8 -*-

from models import User, Stat


def create_new_user(user_info):
    new_user = User(username=user_info['username'], bio=user_info['bio'],
                    website=user_info['website'], profile_picture=user_info['profile_picture'],
                    user_id=user_info['id'], full_name=user_info['full_name'])
    user_stat = Stat(followed_by=user_info['counts']['followed_by'],
                     follows=user_info['counts']['follows'],
                     media=user_info['counts']['media'])
    new_user.stat = user_stat

    user_stat.save()
    new_user.save()
    return new_user
