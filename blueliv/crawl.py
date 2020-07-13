"""
Crawl module allows to search and crawl information.

"""
from .configuration import BASE_CRAWL_URL
from .core import BluelivRequest


class CrawlerRequest(BluelivRequest):
    """
    Class to be able to deal with the requests to crawl information.

    """
    term: str = None
    is_text: bool = False

    def __init__(self, **kwargs):
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

        if 'limit' in kwargs:
            self.limit = kwargs.get('limit', None)

        if 'since_id' in kwargs:
            self.is_text = kwargs.get('since_id', False)

        super().__init__(token=self._custom_token,
                         base_url=self._base_url,
                         category=self._category,
                         limit=self.limit,
                         since_id=self.since_id)

    def crawl(self, term: str, is_text: bool = False):
        """
        Crawl method to search for a term (or url).

        :param term: the term or url we are looking for.
        :param is_text: if it is text, please set to True (otherwise is URL)
        :return:
        """
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
