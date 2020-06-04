from .configuration import BASE_CRAWL_URL
from .core import BluelivRequest


class CrawlerRequest(BluelivRequest):
    _category = None
    _base_url = None
    term = None
    is_text = False

    def __init__(self, *args, **kwargs):
        self._category = 'crawl'
        self._base_url = '/crawl'
        self.term = None
        self.is_text = False

        if 'token' in kwargs:
            self._custom_token = kwargs.get('token', None)

        if 'base_url' in kwargs:
            self._base_url = kwargs.get('base_url', '/crawl')
        else:
            self._base_url = BASE_CRAWL_URL

        if 'term' in kwargs:
            self.term = kwargs.get('term', None)

        if 'is_text' in kwargs:
            self.is_text = kwargs.get('is_text', False)

        super().__init__(token=self._custom_token)

    def crawl(self, term: str, is_text: bool = False):
        data = {
            'url': term,
            'text': is_text
        }

        resource_url = self._base_url

        results = self.request(resource=resource_url,
                               use_post=True,
                               data=data,
                               json_format=True)

        return results
