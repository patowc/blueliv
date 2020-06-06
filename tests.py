"""
Tests module for blue   liv package.

The following tests are divided in tests cases per contexts:

    Enviroment: configuration and env variables.
    Models: testing all models are working as expected.
    RemoteEndpoint: test to verify the API url is alive.

"""
import os
import unittest

try:
    import requests
except ModuleNotFoundError:
    print('- requests not available so we are not using requests tests.')
    requests = None

try:
    import responses
except ModuleNotFoundError:
    print('- responses not available so we are not using requests tests.')
    responses = None

from api.configuration import (
    DEBUG, VERSION,
    BASE_API_URL,
    BASE_SEARCH_URL,
    BASE_USERS_URL, BASE_USERS_SPARKS_URL, BASE_USERS_IOCS_URL,
    BASE_SPARKS_URL, BASE_SPARKS_TIMELINE_URL, BASE_SPARKS_DISCOVER_URL,
    BASE_SPARKS_IOCS_URL, BASE_IOCS_URL, BASE_IOCS_TYPES_URL,
    BASE_IOCS_TIMELINE_URL, BASE_IOCS_DISCOVER_URL,
    BASE_TAGS_URL, BASE_TAGS_SPARKS_URL, BASE_TAGS_IOCS_URL,
    BASE_CRAWL_URL,
    BASE_MALWARES_URL, BASE_MALWARES_UPLOAD_URL,
    TOKEN, AUTHORIZATION_HEADER, AUTHORIZATION
)
from api.core import BASEModel, BASERequestModel, BluelivRequest
from api.crawl import CrawlerRequest
from api.iocs import BluelivIOC, IocsRequest
from api.malwares import BluelivMalware, MalwaresRequest
from api.sparks import Spark, SparksRequest
from api.tags import Tag, TagsRequest
from api.users import BluelivUser, UsersRequest


class EnvironmentTests(unittest.TestCase):
    def test_configuration(self):
        self.assertEqual(DEBUG, False)
        self.assertEqual(VERSION, 'v1')
        self.assertEqual(TOKEN, 'invalid-token')
        self.assertEqual(BASE_API_URL, 'https://community.blueliv.com/api/v1')
        self.assertEqual(AUTHORIZATION_HEADER, 'Authorization')
        self.assertEqual(AUTHORIZATION, 'Token invalid-token')
        self.assertEqual(BASE_SPARKS_URL, '/sparks')
        self.assertEqual(BASE_SPARKS_TIMELINE_URL, '/timeline')
        self.assertEqual(BASE_SPARKS_DISCOVER_URL, '/discover')
        self.assertEqual(BASE_SPARKS_IOCS_URL, '/iocs')
        self.assertEqual(BASE_IOCS_URL, '/iocs')
        self.assertEqual(BASE_IOCS_TYPES_URL, '/iocs/types')
        self.assertEqual(BASE_IOCS_TIMELINE_URL, '/timeline')
        self.assertEqual(BASE_IOCS_DISCOVER_URL, '/discover')
        self.assertEqual(BASE_TAGS_URL, '/tags')
        self.assertEqual(BASE_TAGS_SPARKS_URL, '/sparks')
        self.assertEqual(BASE_TAGS_IOCS_URL, '/iocs')
        self.assertEqual(BASE_USERS_URL, '/users')
        self.assertEqual(BASE_USERS_SPARKS_URL, '/sparks')
        self.assertEqual(BASE_USERS_IOCS_URL, '/iocs')
        self.assertEqual(BASE_CRAWL_URL, '/crawl')
        self.assertEqual(BASE_MALWARES_URL, '/malwares')
        self.assertEqual(BASE_MALWARES_UPLOAD_URL, '/upload')
        self.assertEqual(BASE_SEARCH_URL, '/search')

    def test_environment(self):
        os.environ['BLUELIV_API_DEBUG'] = 'True'
        DEBUG = os.getenv('BLUELIV_API_DEBUG', False)
        self.assertEqual(DEBUG, 'True')


class ModelsTests(unittest.TestCase):
    def test_core_models(self):
        base_model = BASEModel()
        self.assertNotEqual(base_model, None)

        counter = base_model.get_instance_counter()
        self.assertEqual(counter, 1)  # every new instance increments counter.

        base_request_model = BASERequestModel(token='testing-token')
        self.assertNotEqual(base_request_model, None)

        blueliv_request_model = BluelivRequest(token='testing-token-2')
        self.assertNotEqual(blueliv_request_model, None)
        self.assertEqual(blueliv_request_model.get_token(), 'testing-token-2')
        self.assertNotEqual(blueliv_request_model.get_token(), 'testing-token')
        self.assertNotEqual(blueliv_request_model.get_token(), 'invalid-token')

    def test_crawl_models(self):
        crawl_request_model = CrawlerRequest(token='testing-token')
        self.assertNotEqual(crawl_request_model, None)

    def test_iocs_models(self):
        iocs_model = BluelivIOC()
        self.assertNotEqual(iocs_model, None)

        ioc_request_model = IocsRequest(token='testing-token')
        self.assertNotEqual(ioc_request_model, None)

    def test_malwares_models(self):
        malware_model = BluelivMalware()
        self.assertNotEqual(malware_model, None)

        malware_request_model = MalwaresRequest(token='testing-token')
        self.assertNotEqual(malware_request_model, None)

    def test_sparks_models(self):
        spark_model = Spark()
        self.assertNotEqual(spark_model, None)

        sparks_request_model = SparksRequest(token='testing-token')
        self.assertNotEqual(sparks_request_model, None)

    def test_tags_models(self):
        tag_model = Tag()
        self.assertNotEqual(tag_model, None)

        tags_request_model = TagsRequest(token='testing-token')
        self.assertNotEqual(tags_request_model, None)

    def test_users_models(self):
        user_model = BluelivUser()
        self.assertNotEqual(user_model, None)

        users_request_model = UsersRequest(token='testing-token')
        self.assertNotEqual(users_request_model, None)


class RemoteEndpointTests(unittest.TestCase):
    @responses.activate
    def test_fake_request_and_response(self):
        if requests is not None and responses is not None:
            responses.add(**{
                'method': responses.GET,
                'url': BASE_API_URL,
                'body': '{"Blueliv_error": "Fake error"}',
                'status': 404,
                'content_type': 'application/json',
                'adding_headers': {'X-Blueliv-Fake-Header': 'Fake'}
            })

            response = requests.get(BASE_API_URL)

            self.assertEqual({'Blueliv_error': 'Fake error'}, response.json())
            self.assertEqual(404, response.status_code)

    def test_remote_endpoint_is_alive(self):
        valid_response_status = [200, 401, 400]
        url = '{base}/{users}/{me}'.format(base=BASE_API_URL,
                                           users=BASE_USERS_URL,
                                           me='me')
        response = requests.get(url)
        self.assertIn(response.status_code, valid_response_status)


if __name__ == "__main__":
    unittest.main()