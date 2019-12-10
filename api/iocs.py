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
    _base_url = '/iocs'
    _iocs_types_url = '/types'
    limit = None
    since_id = None

    def __init__(self, *args, **kwargs):
        if 'base_url' in kwargs:
            self._base_url = kwargs.get('base_url', '/iocs')
        else:
            self._base_url = configuration.BASE_IOCS_URL

        if 'limit' in kwargs:
            self.limit = kwargs.get('limit', None)

        if 'since_id' in kwargs:
            self.limit = kwargs.get('since_id', None)

        super().__init__()

    def iocs_types(self):
        resource = '%s%s' % (self._base_url,
                             self._iocs_types_url)
        results = self.request(resource=resource)
        return results
