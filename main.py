# -*- coding: utf-8 -*-

import httplib
import json

from furl import furl
import requests

from models import User, Stat, Media


class Instagram(object):
    ACCESS_TOKEN = "487872815.1497896.ef9829ec8bf9414cb7d85967833670b5"
    CLIENT_SECRET = "de0a95bcfb5746f6915e04b1905a73f8"
    BASE_URL = 'https://api.instagram.com/v1'
    SAMPLE_USER = {'id': '487872815', 'sample_media_id': '1211826064585392206_487872815'}

    @staticmethod
    def _parse_response(content):
        content = json.loads(content)
        if content['meta']['code'] != httplib.OK:
            raise Exception('API returned bad response like {}'.format(content['meta']))
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

    def get_user_media(self, user_id):
        url = self._update_url('/users/{}/media/recent'.format(user_id))
        r = requests.get(url)
        response = self._parse_response(r.content)
        return response

    def get_user_info(self, user_id):
        url = self._update_url('/users/{}/'.format(user_id))
        r = requests.get(url)
        response = self._parse_response(r.content)
        return response


if __name__ == '__main__':
    i = Instagram()

    likes = dict()

    # Get user info
    # sample_user_data = i.get_user_info(i.SAMPLE_USER['id'])
    # print 'User data - {}'.format(sample_user_data)

    # Get last media of the sample user
    medias = i.get_user_media(i.SAMPLE_USER['id'])

    for media in medias:
        likes[media['id']] = i.get_media_likes(media['id'])

    for media_id, users in likes.iteritems():
        media = Media(media_id=media_id)
        media.save()
        for user in users:
            user_info = i.get_user_info(user['id'])
            try:
                user = User.select().where(User.user_id == user_info['id']).get()
            except User.DoesNotExist:
                user = User(username=user_info['username'], bio=user_info['bio'],
                            website=user_info['website'], profile_picture=user_info['profile_picture'],
                            user_id=user_info['id'], full_name=user_info['full_name'])
                user_stat = Stat(followed_by=user_info['counts']['followed_by'],
                                 follows=user_info['counts']['follows'],
                                 media=user_info['counts']['media'])
                user.stat = user_stat

                user_stat.save()
                user.save()
            media.users.add([user])
    
    # print 'Likes of the media with id {} - {}'.format(random_media_id, random_media_likes)
