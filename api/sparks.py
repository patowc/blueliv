import json
from .. import configuration
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
    _sparks_iocs_url = '/iocs'
    _timeline_url = '/timeline'
    _discover_url = '/discover'
    limit = None
    since_id = None

    def __init__(self, *args, **kwargs):
        if 'token' in kwargs:
            self._custom_token = kwargs.get('token', None)

        if 'base_url' in kwargs:
            self._base_url = kwargs.get('base_url', '/sparks')
        else:
            self._base_url = configuration.BASE_SPARKS_URL

        if 'timeline' in kwargs:
            self._timeline_url = kwargs.get('timeline', '/timeline')
        else:
            self._timeline_url = configuration.BASE_SPARKS_TIMELINE_URL

        if 'discover' in kwargs:
            self._discover_url = kwargs.get('discover', '/discover')
        else:
            self._discover_url = configuration.BASE_SPARKS_DISCOVER_URL

        if 'iocs' in kwargs:
            self._sparks_iocs_url = kwargs.get('iocs', '/iocs')
        else:
            self._sparks_iocs_url = configuration.BASE_SPARKS_IOCS_URL

        if 'limit' in kwargs:
            self.limit = kwargs.get('limit', None)

        if 'since_id' in kwargs:
            self.limit = kwargs.get('since_id', None)

        super().__init__(token=self._custom_token)

    def get(self, spark_id):
        resource_url = '%s/%s' % (self._base_url, spark_id)

        results = self.request(resource=resource_url)
        return results

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

    def discover(self, limit=None, since_id=None):
        params = {}
        resource_url = '%s%s' % (self._base_url,
                                 self._discover_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        results = self.request(resource=resource_url,
                               params=params)

        return results

    def iocs(self, spark_id, limit=None, since_id=None):
        params = {}
        resource_url = '%s/%s%s' % (self._base_url,
                                    spark_id,
                                    self._sparks_iocs_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        results = self.request(resource=resource_url,
                               params=params)

        return results

    def publish(self, title, description, tlp='green', source_urls=None, source_malware_id=None, tags=None, iocs=None):
        resource_url = self._base_url
        data = dict()

        data['title'] = title
        data['description'] = description
        data['tlp'] = tlp
        if source_urls:
            data['source_urls'] = source_urls

        if source_malware_id:
            data['source_malware_id'] = source_malware_id

        if tags:
            data['tags'] = tags

        if iocs:
            data['iocs'] = iocs

        results = self.request(resource=resource_url,
                               POST=True,
                               data=data,
                               json_format=True)
        return results
