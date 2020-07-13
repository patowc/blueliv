"""
Module to deal and manage IoCs.

"""
import typing

from .configuration import (
    BASE_IOCS_URL, BASE_IOCS_TIMELINE_URL, BASE_IOCS_DISCOVER_URL
)

from .core import BASEModel, BluelivRequest


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


class BluelivIOC(BASEModel):  # pylint: disable=too-few-public-methods
    """
    Model to store IOC information.

    """
    spark_id = None
    ioc_id = None
    content = None
    ioc_type = None
    ioc_subtype = None
    created_at = None

    def __init__(self, **kwargs):
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


class IocsRequest(BluelivRequest):
    """
    Model to be able to deal with IoC requests.

    """
    _iocs_types_url: str = '/types'
    _iocs_timeline_url: str = '/timeline'
    _iocs_discover_url: str = '/discover'
    limit: typing.Optional[str] = None
    since_id: typing.Optional[str] = None

    def __init__(self, **kwargs):
        self._category = 'iocs'
        self._base_url = '/iocs'
        self._iocs_types_url = '/types'
        self._iocs_timeline_url = '/timeline'
        self._iocs_discover_url = '/discover'
        self.limit = None
        self.since_id = None

        if 'token' in kwargs:
            self._custom_token = kwargs.get('token', None)

        if 'base_url' in kwargs:
            self._base_url = kwargs.get('base_url', '/iocs')
        else:
            self._base_url = BASE_IOCS_URL

        if 'category' in kwargs:
            self._category = kwargs.get('category', 'iocs')

        if 'timeline' in kwargs:
            self._iocs_timeline_url = kwargs.get('timeline', '/timeline')
        else:
            self._iocs_timeline_url = BASE_IOCS_TIMELINE_URL

        if 'discover' in kwargs:
            self._iocs_discover_url = kwargs.get('discover', '/discover')
        else:
            self._iocs_discover_url = BASE_IOCS_DISCOVER_URL

        if 'limit' in kwargs:
            self.limit = kwargs.get('limit', None)

        if 'since_id' in kwargs:
            self.is_text = kwargs.get('since_id', False)

        super().__init__(token=self._custom_token,
                         base_url=self._base_url,
                         category=self._category,
                         limit=self.limit,
                         since_id=self.since_id)

    def _private_request(self, resource_url: str, params: dict):
        """
        This is a wrapper method to reduce code and make it cleaner.

        :param resource_url: the url to send the request.
        :param params: all the parameters for the request.
        :return: dict, list or JSON.
        """
        return self.request(resource=resource_url,
                            params=params)

    def types(self):
        """
        Retrieve a list of available types on the Community.

        :return: dict, list or JSON.
        """
        resource = '%s%s' % (self._base_url,
                             self._iocs_types_url)
        results = self.request(resource=resource)
        return results

    def timeline(self, limit=None, since_id=None):
        """
        Retrieve the latest IoCs with a timestamp mark.

        :param limit: the maximum number of item we want to receive.
        :param since_id: the reference since we want to get the information.
        :return: list, dict or JSON.

        """
        params = {}

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        resource_url = '%s%s' % (self._base_url,
                                 self._iocs_timeline_url)

        return self._private_request(resource_url=resource_url,
                                     params=params)

    def discover(self, limit=None, since_id=None):
        """
        Retrieve the latest sparks and IoC information published.

        :param limit: the maximum number of item we want to receive.
        :param since_id: the reference since we want to get the information.
        :return: list, dict or JSON.

        """
        params = {}
        resource_url = '%s%s' % (self._base_url,
                                 self._iocs_discover_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        return self._private_request(resource_url=resource_url,
                                     params=params)
