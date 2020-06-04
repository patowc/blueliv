import requests
import json

from . import configuration


class BASEModel:
    _instance_counter = 0

    def __init__(self):
        self._instance_counter += 1


class BASERequestModel:
    version = None
    token = None

    def __init__(self):
        self.version = configuration.VERSION
        self.token = 'invalid-token'


class BluelivRequest(BASERequestModel):
    _category = None
    _url = None
    _base_url = None
    _custom_token = None
    _authorization_header = None
    _authorization = None
    _headers = {}
    _allowed_categories = []
    _last_url_invoked = None
    last_response = None
    request_count = 0

    def __init__(self, token: str = None):
        self._category = 'core'
        self._url = ''
        self._base_url = ''
        self._custom_token = None
        self._authorization_header = 'Authorization'
        self._authorization = 'Token invalid-token'
        self._headers = {}
        self._allowed_categories = ['iocs', 'sparks', 'tags']
        self._last_url_invoked = None
        self.last_response = None
        self.request_count = 0

        if configuration.DEBUG is True:
            print('Token[%s]' % token)

        self._url = configuration.BASE_API_URL
        self._authorization_header = configuration.AUTHORIZATION_HEADER
        if not token:
            self.token = configuration.TOKEN
            self._authorization = configuration.AUTHORIZATION
            if configuration.DEBUG is True:
                print('Token parameter was None. ENV-Token[%s]' % self.token)
                print('Authorization header [%s]' % self._authorization)
        else:
            self._authorization = configuration.AUTHORIZATION_FORMAT % token
            self._custom_token = token
            self.token = token

        self._headers = {self._authorization_header: self._authorization}
        super().__init__()

    def _increment_count(self):
        self.request_count += 1

    def _decrement_count(self):
        self.request_count -= 1

    def request(self, *args, **kwargs):
        resource = None
        search_type = None
        params = None
        POST = False
        data = None
        json_format = False
        files = None
        as_json = False

        if 'resource' in kwargs:
            resource = kwargs.get('resource', None)

        if 'search_type' in kwargs:
            search_type = kwargs.get('search_type', None)

        if 'params' in kwargs:
            params = kwargs.get('params', None)

        if 'POST' in kwargs:
            POST = kwargs.get('POST', False)

        if 'data' in kwargs:
            data = kwargs.get('data', None)

        if 'json_format' in kwargs:
            json_format = kwargs.get('json_format', False)

        if 'files' in kwargs:
            files = kwargs.get('files', None)

        if 'as_json' in kwargs:
            as_json = kwargs.get('as_json', False)

        if configuration.DEBUG is True:
            print('> BluelivRequest.request called.')

        if POST is True and data is None:
            raise Exception('If POST = True, must provide data (was None).')

        if POST is False and data is True:
            raise Exception('If POST = False, data must be None (default).')

        r = None
        self._increment_count()
        url = self._url
        if resource:
            url = '%s%s' % (url,
                            resource)

        if search_type:
            url = '%s/%s' % (url,
                             search_type)

        self._last_url_invoked = url

        if configuration.DEBUG is True:
            print('> BluelivRequest.request for compound url [%s].' % url)

        if files:
            POST = True
            json_format = False

        if configuration.DEBUG is True:
            print('request with Headers [%s].' % self._headers)

        if not params:
            if configuration.DEBUG is True:
                print('request called with no params parameter.')

            if POST is False:
                if configuration.DEBUG is True:
                    print('request POST is False.')

                r = requests.get(url, headers=self._headers)
            else:
                if configuration.DEBUG is True:
                    print('request POST is True.')

                if json_format is True:
                    if configuration.DEBUG is True:
                        print('request POST is True: [JSON FORMAT]')

                    r = requests.post(url, headers=self._headers, json=data)
                else:
                    if files:
                        r = requests.post(url,
                                          headers=self._headers,
                                          files=files)
                    else:
                        r = requests.post(url,
                                          headers=self._headers,
                                          data=data)
        else:
            if configuration.DEBUG is True:
                print('request called with params: [%s].' % str(params))

            if POST is False:
                if configuration.DEBUG is True:
                    print('request POST is False.')

                r = requests.get(url, headers=self._headers, params=params)
            else:
                if configuration.DEBUG is True:
                    print('request POST is False.')

                if json_format is True:
                    if configuration.DEBUG is True:
                        print('request POST is True: [JSON FORMAT].')

                    r = requests.post(url,
                                      headers=self._headers,
                                      params=params,
                                      json=data)
                else:
                    if files:
                        r = requests.post(url,
                                          headers=self._headers,
                                          params=params,
                                          files=files)
                    else:
                        r = requests.post(url,
                                          headers=self._headers,
                                          params=params,
                                          data=data)

        if r.status_code == 200:
            if configuration.DEBUG is True:
                print('request RESULT STATUS [200]. OK.')

            result = r.json()
            if result:
                if as_json is True:
                    return result
                else:
                    return json.dumps(result)
            else:
                return None
        elif r.status_code == 400:
            if configuration.DEBUG is True:
                print('> BluelivRequest.request RESULT STATUS [400]. ERROR.')

            raise Exception('[%s]: Error in request [%d]: %s' % (url,
                                                                 r.status_code,
                                                                 r.content))

        elif r.status_code == 422:
            if configuration.DEBUG is True:
                print('request RESULT STATUS [422]. ERROR.')

            raise Exception('[%s]: Error in term [%d]: %s' % (url,
                                                              r.status_code,
                                                              str(r.content)))
        else:
            if configuration.DEBUG is True:
                print('request STATUS [%d]. UNEXPECTED.' % r.status_code)
            raise Exception('[%s]: Exception code [%d]' % (url,
                                                           r.status_code))

    def search(self,
               search_term: str,
               tag: str = None,
               limit: int = 0,
               since_id: int = 0,
               as_json: bool = True):
        if self._category == 'core':
            raise Exception('CORE is not searchable.')

        if self._category not in self._allowed_categories:
            raise Exception('Categories for search are: iocs, sparks, tags.')

        params = {'search': search_term}
        if tag:
            params['tag'] = tag

        if limit > 0:
            params['limit'] = limit

        if since_id > 0:
            params['since_id'] = since_id

        results = self.request(resource=configuration.BASE_SEARCH_URL,
                               search_type=self._category,
                               POST=False,
                               params=params,
                               as_json=as_json)

        return results
