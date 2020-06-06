"""
Core will define the base classes and methods available for the whole API
package.

"""
import typing
import json
import requests

from .configuration import (
    DEBUG,
    VERSION,
    BASE_API_URL, BASE_SEARCH_URL,
    TOKEN,
    AUTHORIZATION, AUTHORIZATION_FORMAT, AUTHORIZATION_HEADER
)


class BASEModel:
    """BASEModel is the root class for all models in the package. Focused in
    storing the details about a model, not to implement actions.

    To track instances count, we are using an attribute _instance_counter that
    will increment a counter whenever a new instance is created.

    Attributes:
        _instance_counter: the counter to track instance count.

    Todo:
        * Potentially remove the _instance_counter. In evaluation phase.

    .. _Google Python Style Guide:
        http://google.github.io/styleguide/pyguide.html

    """

    # pylint: disable=too-few-public-methods
    # Base model (consider it as an interface)

    _instance_counter = 0

    def __init__(self):
        '''Increment instance counter when constructor is invoked.

        This is a potential element to be removed, as it may have no use.
        '''
        self._instance_counter += 1

    def get_instance_counter(self):
        """
        A getter for the instance counter.
        :return: _instance_counter
        """
        return self._instance_counter


class BASERequestModel:
    """BASERequestModel is the root class for any request based module. This
    means that every module performing API requests will be derived from it.

    It has two main attributes:

    Attributes:
        version: where we will track the API version (will be taken from the
        configurations).

        token: the API token set to access the API.

    """

    # pylint: disable=too-few-public-methods
    # Base model (consider it as an interface)

    version: str = None
    token: str = None

    def __init__(self, token: str):
        self.version = VERSION
        # token is set to a fixed, invalid, string initially.
        self.token = token

    def get_token(self):
        """
        A getter for the token value in the request class.

        :return: token value
        """
        return self.token

    def get_version(self):
        """
        A getter for the version value in the request class.

        :return: token value
        """
        return self.version


class BluelivRequest(BASERequestModel):
    """BluelivRequest is a generic class that may request resources from the
    remote API. Is like having a raw request class where we can set in a
    manual way the destination urls to connect, and the resources to be
    processed.

    It has several attributes to be configured:

    Attributes:
        _category: this is the category of request we are performing. Within
        the following: iocs, sparks, tags.

        _url: the final url that the request is sent. It is built along the
        functions and variables in the specific invocation.

        _base_url: this is the base resource for the final url, for example
        if you are dealing with users, _base_url will be 'users'

        _custom_token: when the token is passed in an explicit way (from the
        constructor parameters) it will be stored here. Then, it will be
        copied to the _token attribute.

        _authorization_header: which is the header we have to use when sending
        the request to the remote endpoint. We are ready to change if the API
        changes (for example, from Token to Bearer or something similar).

        _authorization: is the final Authorization string that will be set.

        _headers: a dictionary with extra headers that are going to be passed
        to the request.

        _allowed_categories: a list of the categories that can be configured,
        as in the _category attribute.

        _last_url_invoked: an attribute we can use for debugging purposes. It
        will store the url from the last request.

        request_count: a counter for the request being sent.

        limit: a parameter to limit the number of items to be retrieved.

        since_id: a reference mark from a previous request or time position,
        so all results retrieved will not be older that this reference.

    """

    # pylint: disable=too-many-instance-attributes
    # 13 elements, but are all used.

    _category: typing.Optional[str] = None
    _url: typing.Optional[str] = None
    _base_url: typing.Optional[str] = None
    _custom_token: typing.Optional[str] = None
    _authorization_header: typing.Optional[str] = None
    _authorization: typing.Optional[str] = None
    _headers: dict = {}
    _allowed_categories: list = []
    _last_url_invoked: typing.Optional[str] = None
    last_response: typing.Optional[str] = None
    request_count: int = 0
    limit: typing.Optional[str] = None
    since_id: typing.Optional[str] = None

    def __init__(self, **kwargs):
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
        self.limit = None
        self.since_id = None

        # If token is present in kwargs, we set it.
        if 'token' in kwargs:
            # Default value for token is None. It is set onto _custom_token
            self._custom_token = kwargs.get('token', None)

        # If category is present in kwargs, we set it.
        if 'category' in kwargs:
            # Default value for category is 'core'.
            self._category = kwargs.get('category', 'core')

        # If no _custom_token, we will set the default from configuration.
        # TOKEN may have a value taken from the environment.
        if not self._custom_token:
            self._custom_token = None
            self.token = TOKEN
            # We get AUTHORIZATION from the configuration (as the full string
            # is built there.
            self._authorization = AUTHORIZATION
            if DEBUG is True:
                print('Token parameter was None. ENV-Token[%s]' % self.token)
                print('Authorization header [%s]' % self._authorization)
        else:
            self._authorization = AUTHORIZATION_FORMAT % self._custom_token
            self.token = self._custom_token

        if 'base_url' in kwargs:
            self._base_url = kwargs.get('base_url', '')

        if 'limit' in kwargs:
            self.limit = kwargs.get('limit', None)

        if 'since_id' in kwargs:
            self.since_id = kwargs.get('since_id', None)

        self._url = BASE_API_URL
        self._authorization_header = AUTHORIZATION_HEADER
        self._headers = {self._authorization_header: self._authorization}

        super().__init__(token=self.token)

    def get_category(self):
        """
        A getter to retrieve the category value.

        :return: category value (_category)
        """
        return self._category

    def request(self, **kwargs):
        """
        Request method is the base method to be able to retrieve from Blueliv
        endpoint in the API.

        :param resource: the url we are going to connect to.
        :param search_type: the resource category we search for or retrieve.
        :param params: search or request params.
        :param use_post: if POST method will be used (True).
        :param data: data to be posted (use_post must be True).
        :param json_format: if data (see data) is in JSON format.
        :param files: the files we want to include in the request.
        :param as_json: if we want to receive the response as JSON (True).
        :return: dict or JSON (if as_json ==  True) with the results.

        """
        resource = None
        search_type = None
        params = None
        use_post = False
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

        if 'use_post' in kwargs:
            use_post = kwargs.get('use_post', False)

        if 'data' in kwargs:
            data = kwargs.get('data', None)

        if 'json_format' in kwargs:
            json_format = kwargs.get('json_format', False)

        if 'files' in kwargs:
            files = kwargs.get('files', None)

        if 'as_json' in kwargs:
            as_json = kwargs.get('as_json', False)

        if DEBUG is True:
            print('request called.')

        if use_post is True and data is None:
            raise Exception('If use_post=True, must provide data (was None)')

        if use_post is False and data is True:
            raise Exception('If use_post=False, data must be None (default)')

        res = None
        url = self._url
        if resource:
            url = '%s%s' % (url,
                            resource)

        if search_type:
            url = '%s/%s' % (url,
                             search_type)

        self._last_url_invoked = url

        if DEBUG is True:
            print('request for compound url [%s].' % url)

        if files:
            use_post = True
            json_format = False

        if DEBUG is True:
            print('request with Headers [%s].' % self._headers)

        if not params:
            if DEBUG is True:
                print('request called with no params parameter.')

            if use_post is False:
                if DEBUG is True:
                    print('request use_post is False.')

                res = requests.get(url, headers=self._headers)
            else:
                if DEBUG is True:
                    print('request POST is True.')

                if json_format is True:
                    if DEBUG is True:
                        print('request use_post is True: [JSON FORMAT]')

                    res = requests.post(url, headers=self._headers, json=data)
                else:
                    if files:
                        res = requests.post(url,
                                            headers=self._headers,
                                            files=files)
                    else:
                        res = requests.post(url,
                                            headers=self._headers,
                                            data=data)
        else:
            if DEBUG is True:
                print('request called with params: [%s].' % str(params))

            if use_post is False:
                if DEBUG is True:
                    print('request use_post is False.')

                res = requests.get(url,
                                   headers=self._headers,
                                   params=params)
            else:
                if DEBUG is True:
                    print('request POST is False.')

                if json_format is True:
                    if DEBUG is True:
                        print('request use_post is True: [JSON FORMAT].')

                    res = requests.post(url,
                                        headers=self._headers,
                                        params=params,
                                        json=data)
                else:
                    if files:
                        res = requests.post(url,
                                            headers=self._headers,
                                            params=params,
                                            files=files)
                    else:
                        res = requests.post(url,
                                            headers=self._headers,
                                            params=params,
                                            data=data)

        if res.status_code == 200:
            if DEBUG is True:
                print('request RESULT STATUS [200]. OK.')

            result = res.json()
            if result:
                if as_json is True:
                    return result
                return json.dumps(result)
            return None
        elif res.status_code == 400:
            if DEBUG is True:
                print('request RESULT STATUS [400]. ERROR.')

            raise Exception('[%s]: Error request [400]: %s' % (url,
                                                               res.content))
        elif res.status_code == 422:
            if DEBUG is True:
                print('request RESULT STATUS [422]. ERROR.')

            raise Exception('[%s]: Error request [422]: %s' % (url,
                                                               res.content))

        if DEBUG is True:
            print('request STATUS [%d]. UNEXPECTED.' % res.status_code)

        raise Exception('[%s]: Exception code [%d]' % (url,
                                                       res.status_code))

    def search(self,  # pylint: disable=too-many-arguments
               search_term: str,
               tag: str = None,
               limit: int = 0,
               since_id: int = 0,
               as_json: bool = True):
        """
        This is the search method that will be available for all subclasses
        that inherit from the core one.

        :param search_term: the term we want to search.
        :param tag: if we are searching a tag, the tag we want to searcg.
        :param limit: the maximum number of items we want to receive.
        :param since_id: the reference id from we want to receive results.
        :param as_json: if we want the response as a JSON document.
        :return: the results as list or JSON.

        """
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

        results = self.request(resource=BASE_SEARCH_URL,
                               search_type=self._category,
                               POST=False,
                               params=params,
                               as_json=as_json)

        return results
