"""
Sparks are pieces of information with IoC, URLs and other associated assets.

We can search using the API and by term, tag or other parameters.

"""
import typing
from .configuration import (
    BASE_SPARKS_URL, BASE_SPARKS_TIMELINE_URL, BASE_SPARKS_DISCOVER_URL
)

from .core import BASEModel, BluelivRequest


class Spark(BASEModel):  # pylint: disable=too-few-public-methods
    """
    This is the base class to hold Spark data (derived from BASEModel).

    """

    # pylint: disable=too-many-instance-attributes
    # 17 elements, but are all used.

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
    """
    A class to be able to deal with Sparks (retrieve and publish).

    """

    # pylint: disable=too-many-instance-attributes
    # 7 elements, but are all used.

    _category: str = ''
    _base_url: str = ''
    _sparks_iocs_url: str = ''
    _timeline_url: str = ''
    _discover_url: str = ''

    def __init__(self, **kwargs):
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
            self._base_url = BASE_SPARKS_URL

        if 'category' in kwargs:
            self._category = kwargs.get('category', 'sparks')

        if 'timeline' in kwargs:
            self._timeline_url = kwargs.get('timeline', '/timeline')
        else:
            self._timeline_url = BASE_SPARKS_TIMELINE_URL

        if 'discover' in kwargs:
            self._discover_url = kwargs.get('discover', '/discover')
        else:
            self._discover_url = BASE_SPARKS_DISCOVER_URL

        if 'limit' in kwargs:
            self.limit = kwargs.get('limit', None)

        if 'since_id' in kwargs:
            self.is_text = kwargs.get('since_id', False)

        super().__init__(token=self._custom_token,
                         base_url=self._base_url,
                         category=self._category,
                         limit=self.limit,
                         since_id=self.since_id)

    def get(self,
            spark_id: str):
        """
        Quick get to retrieve a Spark by its id.

        :param spark_id: the spark id we want to retrieve.
        :return: list, dict or JSON with the data.

        """
        resource_url = '%s/%s' % (self._base_url, spark_id)
        return self.request(resource=resource_url)

    def timeline(self,
                 limit: typing.Optional[str] = None,
                 since_id: typing.Optional[str] = None):
        """
        Retrieve sparks ordered in a timeline, with timestamp info.

        :param limit: the maximum number of item we want to receive.
        :param since_id: the reference since we want to get the information.
        :return: list, dict or JSON.

        """
        params = {}
        resource_url = '%s%s' % (self._base_url,
                                 self._timeline_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        return self.request(resource=resource_url,
                            params=params)

    def discover(self,
                 limit: typing.Optional[str] = None,
                 since_id: typing.Optional[str] = None):
        """
        Discover will retrieve the latest relevant informations that can be
        found in the Bluelivs community.

        :param limit: the maximum number of item we want to receive.
        :param since_id: the reference since we want to get the information.
        :return: list, dict or JSON.

        """
        params = {}
        resource_url = '%s%s' % (self._base_url,
                                 self._discover_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        return self.request(resource=resource_url,
                            params=params)

    def iocs(self,
             spark_id,
             limit: typing.Optional[str] = None,
             since_id: typing.Optional[str] = None):
        """
        iocs will retrieve the relevant IoCs for an specific spark, set by
        the spark_id.

        :param spark_id: the id for the Spark.
        :param limit: the maximum number of item we want to receive.
        :param since_id: the reference since we want to get the information.
        :return: list, dict or JSON.

        """
        params = {}
        resource_url = '%s/%s%s' % (self._base_url,
                                    spark_id,
                                    self._sparks_iocs_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        return self.request(resource=resource_url,
                            params=params)

    def publish(self, title: str, description: str,
                tlp: str = 'green',
                source_urls: typing.Optional[list] = None,
                source_malware_id: str = None,
                tags: typing.Optional[list] = None,
                iocs: typing.Optional[list] = None):
        """
        Publish let you share your information onto the community (as a Spark)

        :param title: the title for your Spark.
        :param description: details and description.
        :param tlp: from red (restricted) to green (open and use freely).
        :param source_urls: URLs that are relevant.
        :param source_malware_id: a reference malware id if we know it.
        :param tags: tags we want to add to the Spark.
        :param iocs: related IoCs.
        :return: dict, list or JSON.
        """

        # pylint: disable=too-many-arguments

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

        return self.request(resource=resource_url,
                            use_post=True,
                            data=data,
                            json_format=True)
