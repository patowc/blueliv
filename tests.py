import os
import unittest

import requests

from api.configuration import *
from api.core import *


class PackageTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
