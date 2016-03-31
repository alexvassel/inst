# -*- coding: utf-8 -*-
import httplib
import json

from furl import furl
import requests


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
        print url
        r = requests.get(url)
        response = self._parse_response(r.content)
        return response


i = Instagram()

# i.get_user_info(i.SAMPLE_USER['id'])
media = i.get_user_media(i.SAMPLE_USER['id'])[0]['id']
print 'Likes of the media with id {} - {}'.format(media, i.get_media_likes(media))
