# -*- coding: utf-8 -*-

import httplib
import json
import sys

from furl import furl
import requests

from models import User, Stat, Media


class Instagram(object):
    ACCESS_TOKEN = "487872815.5540849.0079521f39ae40ab96fe7403dde3331d"
    CLIENT_SECRET = "b7d2d7585fc047eb9dd6ae7d6c651e4e"
    BASE_URL = 'https://api.instagram.com/v1'

    @staticmethod
    def _parse_response(content):
        content = json.loads(content)
        if content['meta']['code'] != httplib.OK:
            raise TypeError('API returned bad response like {}'.format(content['meta']))
        return content['data']

    def _update_url(self, url):
        url = furl(self.BASE_URL + url)
        url.args['access_token'] = self.ACCESS_TOKEN
        return url

    def get_media_likes(self, media_id):
        url = self._update_url('/media/{}/likes'.format(media_id))
        r = requests.get(url)
        response = self._parse_response(r.content)
        return response

    def get_user_info(self, user_id):
        url = self._update_url('/users/{}/'.format(user_id))
        r = requests.get(url)
        response = self._parse_response(r.content)
        return response

    def get_all_medias(self, user_id):
        result = []
        max_id = 0
        while True:
            url = self._update_url(('/users/{}/media/recent?&max_id={}'
                                    .format(user_id, max_id)))
            r = requests.get(url)
            response = self._parse_response(r.content)
            if not response:
                break
            result.extend(response)
            max_id = response[-1]['id']
        return result

    def get_user_id_by_username(self, username):
        url = self._update_url('/users/search?q={}'.format(username))
        r = requests.get(url)
        response = self._parse_response(r.content)
        user_id = response[0]['id']
        return user_id


def _create_new_user(user_info):
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


if __name__ == '__main__':
    api = Instagram()

    # TODO проверка наличия пользователя
    user_id = api.get_user_id_by_username('frosienka')

    # TODO вывод ошибки в нормальном виде
    # Get all medias of the given user
    try:
        medias = api.get_all_medias(user_id)
    except TypeError as e:
        sys.exit(e.message)

    for media in medias:
        new_media = Media(media_id=media['id'])
        new_media.save()

        # Get all users that liked this media
        media_users = api.get_media_likes(media['id'])

        for user in media_users:
            # Get detailed info about each user liked media
            try:
                user_info = api.get_user_info(user['id'])
            except TypeError as e:
                print e.message
                continue

            try:
                user = User.select().where(User.user_id == user_info['id']).get()
            except User.DoesNotExist:
                user = _create_new_user(user_info)

            new_media.users.add([user])
