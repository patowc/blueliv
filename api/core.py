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
    _category = 'core'
    _url = ''
    _base_url = ''
    _custom_token = None
    _authorization_header = 'Authorization'
    _authorization_value = 'Token invalid-token'
    _headers = {}
    _last_url_invoked = None
    last_response = None
    request_count = 0

    def __init__(self, token=None):
        if configuration.DEBUG is True:
            print('> BluelivRequest.__init__: token[%s]' % token)

        self._url = configuration.BASE_API_URL
        self._authorization_header = configuration.AUTHORIZATION_HEADER
        if not token:
            self.token = configuration.TOKEN
            self._authorization_value = configuration.AUTHORIZATION
            if configuration.DEBUG is True:
                print('> BluelivRequest.__init__: token parameter was None. ENV-Token[%s]' % self.token)
                print('> BluelivRequest.__init__: Authorization header [%s]' % self._authorization_value)
        else:
            self._authorization_value = configuration.AUTHORIZATION_FORMAT % token
            self._custom_token = token
            self.token = token

        self._headers = {self._authorization_header: self._authorization_value}

    def _increment_count(self):
        self.request_count += 1

    def _decrement_count(self):
        self.request_count -= 1

    def request(self, resource=None, search_type=None, params=None, POST=False, data=None, json_format=False, files=None, as_json=False):
        if configuration.DEBUG is True:
            print('> BluelivRequest.request called.')

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
            print('> BluelivRequest.request with Headers [%s].' % self._headers)

        if not params:
            if configuration.DEBUG is True:
                print('> BluelivRequest.request called with no params parameter.')

            if POST is False:
                if configuration.DEBUG is True:
                    print('> BluelivRequest.request POST is False: request.get(url, headers=...)')

                r = requests.get(url, headers=self._headers)
            else:
                if configuration.DEBUG is True:
                    print('> BluelivRequest.request POST is True: request.post(url, ...)')

                if json_format is True:
                    if configuration.DEBUG is True:
                        print('> BluelivRequest.request POST is True: [JSON FORMAT] request.post(url, headers=..., json=data)')

                    r = requests.post(url, headers=self._headers, json=data)
                else:
                    if files:
                        r = requests.post(url, headers=self._headers, files=files)
                    else:
                        r = requests.post(url, headers=self._headers, data=data)
        else:
            if configuration.DEBUG is True:
                print('> BluelivRequest.request called with params parameter: [%s].' % str(params))

            if POST is False:
                if configuration.DEBUG is True:
                    print('> BluelivRequest.request POST is False: request.get(url, headers=..., params=...)')

                r = requests.get(url, headers=self._headers, params=params)
            else:
                if configuration.DEBUG is True:
                    print('> BluelivRequest.request POST is False: request.post(url, ...)')

                if json_format is True:
                    if configuration.DEBUG is True:
                        print('> BluelivRequest.request POST is True: [JSON FORMAT] request.post(url, headers=..., params=params, json=data)')

                    r = requests.post(url, headers=self._headers, params=params, json=data)
                else:
                    if files:
                        r = requests.post(url, headers=self._headers, params=params, files=files)
                    else:
                        r = requests.post(url, headers=self._headers, params=params, data=data)

        if r.status_code == 200:
            if configuration.DEBUG is True:
                print('> BluelivRequest.request RESULT STATUS [200]. OK.')

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

            raise Exception('[%s]: Error in the request (%s): %s' % (url,
                                                                     str(r.status_code),
                                                                     str(r.content)))

        elif r.status_code == 422:
            if configuration.DEBUG is True:
                print('> BluelivRequest.request RESULT STATUS [422]. ERROR.')

            raise Exception('[%s]: Error parsing the term parameter (url) [%s]: %s' % (url,
                                                                                       str(r.status_code),
                                                                                       str(r.content)))
        else:
            raise Exception('[%s]: Exception with error code [%s]' % (url,
                                                                      str(r.status_code)))

    def search(self, search_term, tag=None, limit=0, since_id=0, as_json=True):
        if self._category == 'core':
            raise Exception('CORE is not searchable. Please, invoke search from one of the iocs, sparks or tags subclasses.')

        if self._category != 'iocs' and self._category != 'sparks' and self._category != 'tags:':
            raise Exception('Allowed categories for search are: iocs, sparks and tags. This class is not supported by search yet.')

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
