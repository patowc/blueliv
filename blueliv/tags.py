"""
Tags to manage and dealt with tagged assets and to tag by ourselves.

"""
import typing

from .configuration import (
    BASE_TAGS_URL, BASE_TAGS_SPARKS_URL, BASE_TAGS_IOCS_URL
)

from .core import BASEModel, BluelivRequest


class Tag(BASEModel):  # pylint: disable=too-few-public-methods
    """
    A model to store a tag, with its information.
    """
    tag_id: typing.Optional[str] = None
    name: typing.Optional[str] = None
    questions_count: int = 0
    slug: typing.Optional[str] = None
    sparks_count: int = 0

    def __init__(self):
        self.tag_id = None
        self.name = None
        self.questions_count = 0
        self.slug = None
        self.sparks_count = 0

        super().__init__()


class TagsRequest(BluelivRequest):
    """
    The model to perform and deal with the requests.

    """

    # pylint: disable=too-many-instance-attributes

    _tags_sparks_url: str = ''
    _tags_iocs_url: str = ''
    tag_slug: typing.Optional[str] = None

    def __init__(self, **kwargs):
        self._category = 'tags'
        self._base_url = '/tags'
        self._tags_sparks_url = '/sparks'
        self._tags_iocs_url = '/iocs'
        self.tag_slug = None
        self.limit = None
        self.since_id = None

        if 'token' in kwargs:
            self._custom_token = kwargs.get('token', None)

        if 'base_url' in kwargs:
            self._base_url = kwargs.get('base_url', '/tags')
        else:
            self._base_url = BASE_TAGS_URL

        if 'sparks' in kwargs:
            self._tags_sparks_url = kwargs.get('sparks', '/sparks')
        else:
            self._tags_sparks_url = BASE_TAGS_SPARKS_URL

        if 'iocs' in kwargs:
            self._tags_iocs_url = kwargs.get('iocs', '/iocs')
        else:
            self._tags_iocs_url = BASE_TAGS_IOCS_URL

        if 'tag_slug' in kwargs:
            self.tag_slug = kwargs.get('tag_slug', None)

        if 'limit' in kwargs:
            self.limit = kwargs.get('limit', None)

        if 'since_id' in kwargs:
            self.is_text = kwargs.get('since_id', False)

        super().__init__(token=self._custom_token,
                         base_url=self._base_url,
                         category=self._category,
                         limit=self.limit,
                         since_id=self.since_id)

    def list(self):
        """
        List all the tags in the Community.

        :return: dict, list or JSON with the tag list.
        """
        return self.request(resource=self._base_url)

    def list_sparks(self,
                    tag_slug: str,
                    limit: typing.Optional[str] = None,
                    since_id: typing.Optional[str] = None):
        """
        List sparks tagged with a specific tag.

        :param tag_slug: the tag.
        :param limit: the maximum number of items we want to retrieve.
        :param since_id: the reference id from we want to receive items.
        :return: dict, list or JSON with the sparks.
        """
        params = {}
        resource_url = '%s/%s%s' % (self._base_url,
                                    tag_slug,
                                    self._tags_sparks_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        return self.request(resource=resource_url,
                            params=params)

    def list_iocs(self, tag_slug: str,
                  limit: typing.Optional[str] = None,
                  since_id: typing.Optional[str] = None):
        """
        List IoCs associated with a tag.

        :param tag_slug: the tag.
        :param limit: the maximum number of items we want to retrieve.
        :param since_id: the reference id from we want to receive items.
        :return: dict, list or JSON with the IoCs.

        """
        params = {}
        resource_url = '%s/%s%s' % (self._base_url,
                                    tag_slug,
                                    self._tags_iocs_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        return self.request(resource=resource_url,
                            params=params)
