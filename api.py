# -*- coding: utf-8 -*-

import httplib
import json

from furl import furl
import requests

MAX_ALLOWED_RECORDS = 33


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
            url = self._update_url('/users/{}/media/recent'.format(user_id))
            url.args['max_id'] = max_id
            url.args['count'] = MAX_ALLOWED_RECORDS
            r = requests.get(url)
            response = self._parse_response(r.content)
            if not response:
                break
            result.extend(response)
            max_id = response[-1]['id']
        return result

    def get_user_id_by_username(self, username):
        """returns best matched user"""
        url = self._update_url('/users/search')
        url.args['q'] = username
        r = requests.get(url)
        response = self._parse_response(r.content)
        if not response:
            raise LookupError('No users found with name - {}'.format(username))
        return response[0]['id']
