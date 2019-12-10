import json
from .. import configuration
from .core import BASEModel, BluelivRequest


class Tag(BASEModel):
    tag_id = None
    name = None
    questions_count = 0
    slug = None
    sparks_count = 0


class TagsRequest(BluelivRequest):
    _base_url = '/tags'
    _tags_sparks_url = '/sparks'
    _tags_iocs_url = '/iocs'
    tag_slug = None
    limit = None
    since_id = None

    def __init__(self, *args, **kwargs):
        if 'token' in kwargs:
            self._custom_token = kwargs.get('token', None)

        if 'base_url' in kwargs:
            self._base_url = kwargs.get('base_url', '/tags')
        else:
            self._base_url = configuration.BASE_TAGS_URL

        if 'sparks' in kwargs:
            self._tags_sparks_url = kwargs.get('sparks', '/sparks')
        else:
            self._tags_sparks_url = configuration.BASE_TAGS_SPARKS_URL

        if 'iocs' in kwargs:
            self._tags_iocs_url = kwargs.get('iocs', '/iocs')
        else:
            self._tags_iocs_url = configuration.BASE_TAGS_IOCS_URL

        if 'tag_slug' in kwargs:
            self.tag_slug = kwargs.get('tag_slug', None)

        if 'limit' in kwargs:
            self.limit = kwargs.get('limit', None)

        if 'since_id' in kwargs:
            self.since_id = kwargs.get('since_id', None)

        super().__init__(token=self._custom_token)

    def list(self):
        results = self.request(resource=self._base_url)
        return results

    def list_sparks(self, tag_slug, limit=None, since_id=None):
        params = {}
        resource_url = '%s/%s%s' % (self._base_url,
                                    tag_slug,
                                    self._tags_sparks_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        results = self.request(resource=resource_url,
                               params=params)

        return results

    def list_iocs(self, tag_slug, limit=None, since_id=None):
        params = {}
        resource_url = '%s/%s%s' % (self._base_url,
                                    tag_slug,
                                    self._tags_iocs_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        results = self.request(resource=resource_url,
                               params=params)

        return results
