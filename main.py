# -*- coding: utf-8 -*-


import argparse
import sys

from api import Instagram
from helpers import create_new_user, create_database
from models import User, Media

parser = argparse.ArgumentParser()
parser.add_argument('username', help='username to parse')

args = parser.parse_args()

create_database()

instagram_api = Instagram()

username = args.username

user_id = instagram_api.get_user_id_by_username(username)

print 'starting with user - {}'.format(username)

# Get all medias of the given user
try:
    medias = instagram_api.get_all_medias(user_id)
    print 'total medias count - {}'.format(len(medias))
except TypeError as e:
    sys.exit('Error getting media for the user - {}: {}'.format(username, e.message))


cnt = 0
for media in medias:
    cnt += 1
    print 'processing media {}/{}'.format(cnt, len(medias))
    new_media = Media(media_id=media['id'])
    new_media.save()

    # Get all users that liked this media
    media_users = instagram_api.get_media_likes(media['id'])
    print '---total likes - {}'.format(len(media_users))

    likes_cnt = 0
    for user in media_users:
        likes_cnt += 1
        print '----processing like {}/{}'.format(likes_cnt, len(media_users))
        # Get detailed info about each user liked media
        try:
            user_info = instagram_api.get_user_info(user['id'])
        except TypeError as e:
            print e.message
            continue

        try:
            user = User.select().where(User.user_id == user_info['id']).get()
        except User.DoesNotExist:
            user = create_new_user(user_info)

        new_media.users.add([user])
