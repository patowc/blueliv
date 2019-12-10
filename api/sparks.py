import json
from configuration import *
from .core import BASEModel, BluelivRequest


class Spark(BASEModel):
    spark_id = None
    title = None
    description = None
    tlp = 'red'
    created_at = None
    likes_count = None
    spark_created_at = None
    source_url = []
    weight = None
    geo_domains = []
    geo_ips = []
    geo_points = []
    resparks_count = 0
    iocs_counters = {}
    tags = []
    user = {}
    original_spark = {}


class SparksRequest(BluelivRequest):
    _base_url = '/sparks'
    _timeline_url = '/timeline'
    _discover_url = '/discover'
    _iocs_url = '/iocs'
    limit = None
    since_id = None

    def __init__(self, *args, **kwargs):
        if 'base_url' in kwargs:
            self._base_url = kwargs.get('base_url', '/sparks')
        else:
            self._base_url = BASE_SPARKS_URL

        if 'timeline' in kwargs:
            self._timeline_url = kwargs.get('timeline', '/timeline')
        else:
            self._timeline_url = BASE_SPARKS_TIMELINE_URL

        if 'discover' in kwargs:
            self._discover_url = kwargs.get('discover', '/discover')
        else:
            self._discover_url = BASE_SPARKS_DISCOVER_URL

        if 'iocs' in kwargs:
            self._discover_url = kwargs.get('iocs', '/iocs')
        else:
            self._discover_url = BASE_SPARKS_IOCS_URL

        if 'limit' in kwargs:
            self.limit = kwargs.get('limit', None)

        if 'since_id' in kwargs:
            self.limit = kwargs.get('since_id', None)

        super().__init__()

    def timeline(self, limit=None, since_id=None):
        params = {}
        resource_url = '%s%s' % (self._base_url,
                                 self._timeline_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        results = self.request(resource=resource_url,
                               params=params)

        return results
