from .. import configuration
import requests
import json


class BASEModel:
    _instance_counter = 0

    def __init__(self):
        self._instance_counter += 1


class BASERequestModel:
    version = 'v1'
    token = 'invalid-token'


class BluelivRequest(BASERequestModel):
    _url = ''
    _custom_token = None
    _authorization_header = 'Authorization'
    _authorization_value = 'Token invalid-token'
    _headers = {}
    _last_url_invoked = None
    last_response = None
    request_count = 0

    def __init__(self, token=None):
        self._url = configuration.BASE_API_URL
        self._authorization_header = configuration.AUTHORIZATION_HEADER
        if not token:
            self._authorization_value = configuration.AUTHORIZATION
        else:
            self._authorization_value = configuration.AUTHORIZATION_FORMAT % token
            self._custom_token = token
        self._headers = {self._authorization_header: self._authorization_value}

    def _increment_count(self):
        self.request_count += 1

    def _decrement_count(self):
        self.request_count -= 1

    def request(self, resource=None, params=None, POST=False, data=None):
        if POST is True and data is None:
            raise Exception('If POST is set to True, we must provide data (was None).')

        if POST is False and data is True:
            raise Exception('If POST is set to False (or left by default), data must be None (left by default).')

        r = None
        self._increment_count()
        url = self._url
        if resource:
            url = '%s%s' % (url,
                            resource)
        self._last_url_invoked = url

        if not params:
            if POST is False:
                r = requests.get(url, headers=self._headers)
            else:
                r = requests.post(url, headers=self._headers, data=data)
        else:
            if POST is False:
                r = requests.get(url, headers=self._headers, params=params)
            else:
                r = requests.post(url, headers=self._headers, params=params, data=data)

        if r.status_code == 200:
            result = r.json()
            if result:
                return json.dumps(result)
            else:
                return None
        else:
            raise Exception('[%s]: Exception with error code [%s]' % (url,
                                                                      str(r.status_code)))
