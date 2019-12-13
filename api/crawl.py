import json
from .. import configuration
from .core import BluelivRequest


class CrawlerRequest(BluelivRequest):
    _base_url = '/crawl'
    term = None
    is_text = False

    def __init__(self, *args, **kwargs):
        if 'token' in kwargs:
            self._custom_token = kwargs.get('token', None)

        if 'base_url' in kwargs:
            self._base_url = kwargs.get('base_url', '/crawl')
        else:
            self._base_url = configuration.BASE_CRAWL_URL

        if 'term' in kwargs:
            self.term = kwargs.get('term', None)

        if 'is_text' in kwargs:
            self.is_text = kwargs.get('is_text', False)

        super().__init__(token=self._custom_token)

    def crawl(self, term, is_text=False):
        data = {
            'url': term,
            'text': is_text
        }

        resource_url = self._base_url

        results = self.request(resource=resource_url,
                               POST=True,
                               data=data,
                               json_format=True)

        return results
