from configuration import *
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
    _authorization_header = 'Authorization'
    _authorization_value = 'Token invalid-token'
    _headers = {}
    _iocs_types_url = None
    last_response = None
    request_count = 0

    def __init__(self):
        self._url = BASE_API_URL
        self._authorization_header = AUTHORIZATION_HEADER
        self._authorization_value = AUTHORIZATION
        self._headers = {self._authorization_header: self._authorization_value}
        self._iocs_types_url = BASE_SPARKS_IOCS_TYPES_URL

    def _increment_count(self):
        self.request_count += 1

    def _decrement_count(self):
        self.request_count -= 1

    def request(self, resource=None, params=None):
        r = None
        self._increment_count()
        url = self._url
        if resource:
            url = '%s%s' % (url,
                            resource)

        if not params:
            r = requests.get(url, headers=self._headers)
        else:
            r = requests.get(url, headers=self._headers, params=params)

        if r.status_code == 200:
            result = r.json()
            if result:
                return json.dumps(result)
            else:
                return None
        else:
            raise Exception('[%s]: Exception with error code [%s]' % (url,
                                                                      str(r.status_code)))


class BluelivUser(BASEModel):
    user_id = None
    username = None
    first_name = None
    last_name = None
    karma = None
    badge = None

    def __init__(self, *args, **kwargs):
        if 'user_id' in kwargs:
            self.user_id = kwargs.get('user_id', None)

        if 'username' in kwargs:
            self.username = kwargs.get('username', None)

        if 'first_name' in kwargs:
            self.first_name = kwargs.get('first_name', None)

        if 'last_name' in kwargs:
            self.last_name = kwargs.get('last_name', None)

        if 'karma' in kwargs:
            self.karma = kwargs.get('karma', None)

        if 'badge' in kwargs:
            self.last_name = kwargs.get('badge', None)

        super().__init__()

