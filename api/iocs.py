import json
from .. import configuration
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


class IocsRequest(BluelivRequest):
    _category = 'iocs'
    _base_url = '/iocs'
    _iocs_types_url = '/types'
    _iocs_timeline_url = '/timeline'
    _iocs_discover_url = '/discover'
    limit = None
    since_id = None

    def __init__(self, *args, **kwargs):
        if 'token' in kwargs:
            self._custom_token = kwargs.get('token', None)

        if 'base_url' in kwargs:
            self._base_url = kwargs.get('base_url', '/iocs')
        else:
            self._base_url = configuration.BASE_IOCS_URL

        if 'timeline' in kwargs:
            self._iocs_timeline_url = kwargs.get('timeline', '/timeline')
        else:
            self._iocs_timeline_url = configuration.BASE_IOCS_TIMELINE_URL

        if 'discover' in kwargs:
            self._iocs_discover_url = kwargs.get('discover', '/discover')
        else:
            self._iocs_discover_url = configuration.BASE_IOCS_DISCOVER_URL

        if 'limit' in kwargs:
            self.limit = kwargs.get('limit', None)

        if 'since_id' in kwargs:
            self.limit = kwargs.get('since_id', None)

        super().__init__(token=self._custom_token)

    def types(self):
        resource = '%s%s' % (self._base_url,
                             self._iocs_types_url)
        results = self.request(resource=resource)
        return results

    def timeline(self, limit=None, since_id=None):
        params = {}
        resource_url = '%s%s' % (self._base_url,
                                 self._iocs_timeline_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        results = self.request(resource=resource_url,
                               params=params)

        return results

    def discover(self, limit=None, since_id=None):
        params = {}
        resource_url = '%s%s' % (self._base_url,
                                 self._iocs_discover_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        results = self.request(resource=resource_url,
                               params=params)

        return results
