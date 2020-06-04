from . import configuration
from .core import BASEModel, BluelivRequest


class Spark(BASEModel):
    spark_id = None
    title = None
    description = None
    tlp = None
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

    def __init__(self):
        self.spark_id = None
        self.title = None
        self.description = None
        self.tlp = 'red'
        self.created_at = None
        self.likes_count = None
        self.spark_created_at = None
        self.source_url = []
        self.weight = None
        self.geo_domains = []
        self.geo_ips = []
        self.geo_points = []
        self.resparks_count = 0
        self.iocs_counters = {}
        self.tags = []
        self.user = {}
        self.original_spark = {}

        super().__init__()


class SparksRequest(BluelivRequest):
    _category: str = None
    _base_url: str = None
    _sparks_iocs_url: str = None
    _timeline_url: str = None
    _discover_url: str = None
    limit = None
    since_id = None

    def __init__(self, *args, **kwargs):
        self._category = 'sparks'
        self._base_url = '/sparks'
        self._sparks_iocs_url = '/iocs'
        self._timeline_url = '/timeline'
        self._discover_url = '/discover'
        self.limit = None
        self.since_id = None

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

    def get(self, spark_id: str):
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

    def publish(self, title: str, description: str,
                tlp: str = 'green',
                source_urls=None,
                source_malware_id: str = None,
                tags=None,
                iocs=None):
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
