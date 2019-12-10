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

    def iocs_types(self):
        results = self.request(resource=self._iocs_types_url)
        return results


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


BluelivIOCTypes = (
    (0, 'HASH'),
    (1, 'IPv4'),
    (2, 'URL'),
    (3, 'CVE'),
    (4, 'DOMAIN'),
    (5, 'HOST')
)

BluelivIOCSubtypes = (
    (0, 'Hash-MD5'),
    (1, 'Hash-SHA1'),
    (2, 'Hash-SHA256'),
    (3, 'Hash-SHA512')
)


class BluelivIOC(BASEModel):
    spark_id = None
    ioc_id = None
    content = None
    ioc_type = None
    ioc_subtype = None
    created_at = None

    def __init__(self, *args, **kwargs):
        if 'spark_id' in kwargs:
            self.spark_id = kwargs.get('spark_id', None)

        if 'ioc_id' in kwargs:
            self.ioc_id = kwargs.get('ioc_id', None)

        if 'content' in kwargs:
            self.content = kwargs.get('content', None)

        if 'ioc_type' in kwargs:
            self.ioc_type = kwargs.get('ioc_type', None)

        if 'ioc_subtype' in kwargs:
            self.ioc_subtype = kwargs.get('ioc_subtype', None)

        if 'created_at' in kwargs:
            self.created_at = kwargs.get('created_at', None)

        super().__init__()
