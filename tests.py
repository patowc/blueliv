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

from blueliv.configuration import (
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
from blueliv.core import BASEModel, BASERequestModel, BluelivRequest
from blueliv.crawl import CrawlerRequest
from blueliv.iocs import BluelivIOC, IocsRequest
from blueliv.malwares import BluelivMalware, MalwaresRequest
from blueliv.sparks import Spark, SparksRequest
from blueliv.tags import Tag, TagsRequest
from blueliv.users import BluelivUser, UsersRequest


class EnvironmentTests(unittest.TestCase):
    """
    Tests oriented to verify configuration variables and if they can be set
    through the enviroment.

    """
    def test_configuration(self):
        """
        Test configuration defaults.
        :return: nothing as is a test case.

        """
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
        """
        Test we can retrieve from env, falling back on default values, and
        setting a value in the environment.

        :return: nothing as is a test case.

        """
        os.environ['BLUELIV_API_DEBUG'] = 'True'
        DEBUG = os.getenv('BLUELIV_API_DEBUG', False)
        self.assertEqual(DEBUG, 'True')


class ModelsTests(unittest.TestCase):
    """
    Test oriented to create model instances and verify everything is working
    fine in the constructors.

    """
    def test_core_models(self):
        """
        Test for blueliv.core models.

        :return:  nothing as is a test case.

        """
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
        """
        Test for blueliv.crawl models.

        :return:  nothing as is a test case.

        """
        crawl_request_model = CrawlerRequest(token='testing-token')
        self.assertNotEqual(crawl_request_model, None)

    def test_iocs_models(self):
        """
        Test for iocs.core models.

        :return:  nothing as is a test case.

        """
        iocs_model = BluelivIOC()
        self.assertNotEqual(iocs_model, None)

        ioc_request_model = IocsRequest(token='testing-token')
        self.assertNotEqual(ioc_request_model, None)

    def test_malwares_models(self):
        """
        Test for blueliv.malwares models.

        :return:  nothing as is a test case.

        """
        malware_model = BluelivMalware()
        self.assertNotEqual(malware_model, None)

        malware_request_model = MalwaresRequest(token='testing-token')
        self.assertNotEqual(malware_request_model, None)

    def test_sparks_models(self):
        """
        Test for blueliv.sparks models.

        :return:  nothing as is a test case.

        """
        spark_model = Spark()
        self.assertNotEqual(spark_model, None)

        sparks_request_model = SparksRequest(token='testing-token')
        self.assertNotEqual(sparks_request_model, None)

    def test_tags_models(self):
        """
        Test for blueliv.tags models.

        :return:  nothing as is a test case.

        """
        tag_model = Tag()
        self.assertNotEqual(tag_model, None)

        tags_request_model = TagsRequest(token='testing-token')
        self.assertNotEqual(tags_request_model, None)

    def test_users_models(self):
        """
        Test for blueliv.users models.

        :return:  nothing as is a test case.

        """
        user_model = BluelivUser()
        self.assertNotEqual(user_model, None)

        users_request_model = UsersRequest(token='testing-token')
        self.assertNotEqual(users_request_model, None)


class RemoteEndpointTests(unittest.TestCase):
    """
    Tests oriented to verify the remote API endpoint is working fine.

    """
    @responses.activate
    def test_fake_request_and_response(self):
        """
        This is a fake connection test (using responses package).

        :return: nothing as this is a test case.

        """
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
        """
        This is a real connection test (using requests package). As we don't
        have a valid token inserted, just testing the response is 200, 400 or
        401 that will mean the API endpoint is alive.

        :return: nothing as this is a test case.

        """
        valid_response_status = [200, 400, 401]
        url = '{base}/{users}/{me}'.format(base=BASE_API_URL,
                                           users=BASE_USERS_URL,
                                           me='me')
        response = requests.get(url)
        self.assertIn(response.status_code, valid_response_status)


if __name__ == "__main__":
    unittest.main()
