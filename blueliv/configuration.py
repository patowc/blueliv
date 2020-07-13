"""
Here you will find all configuration variables that can be configured through
the environment.

A quick way to find every available setting is to grep for "ENV_*".

The standard approach here is to set a default value and, then, if
the environment has the proper variable, set again with the value that
was defined in the env.

"""
import os

DEBUG = None
DEBUG = os.getenv('BLUELIV_API_DEBUG',
                  DEBUG)
DEBUG = bool(DEBUG)
# ENV: BLUELIV_API_DEBUG

VERSION = 'v1'
VERSION = os.getenv('BLUELIV_API_VERSION',
                    VERSION)
# ENV: BLUELIV_API_VERSION

TOKEN = 'invalid-token'
TOKEN = os.getenv('BLUELIV_API_TOKEN',
                  TOKEN)
# ENV: BLUELIV_API_TOKEN

BASE_API_URL = 'https://community.blueliv.com/api/%s' % VERSION
BASE_API_URL = os.getenv('BLUELIV_API_BASEURL',
                         BASE_API_URL)
# ENV: BLUELIV_API_BASEURL

AUTHORIZATION_HEADER = 'Authorization'
AUTHORIZATION_HEADER = os.getenv('BLUELIV_API_AUTHORIZATION_HEADER',
                                 AUTHORIZATION_HEADER)
# ENV: BLUELIV_API_AUTHORIZATION_HEADER

AUTHORIZATION_FORMAT = 'Token %s'
AUTHORIZATION_FORMAT = os.getenv('BLUELIV_API_AUTHORIZATION_FORMAT',
                                 AUTHORIZATION_FORMAT)
# ENV: BLUELIV_API_AUTHORIZATION_FORMAT

AUTHORIZATION = AUTHORIZATION_FORMAT % TOKEN

BASE_SPARKS_URL = '/sparks'
BASE_SPARKS_URL = os.getenv('BLUELIV_API_BASE_SPARKS_URL',
                            BASE_SPARKS_URL)
# ENV: BLUELIV_API_BASE_SPARKS_URL

BASE_SPARKS_TIMELINE_URL = '/timeline'
BASE_SPARKS_TIMELINE_URL = os.getenv('BLUELIV_API_BASE_SPARKS_TIMELINE_URL',
                                     BASE_SPARKS_TIMELINE_URL)
# ENV: BASE_SPARKS_TIMELINE_URL

BASE_SPARKS_DISCOVER_URL = '/discover'
BASE_SPARKS_DISCOVER_URL = os.getenv('BLUELIV_API_BASE_SPARKS_DISCOVER_URL',
                                     BASE_SPARKS_DISCOVER_URL)
# ENV: BASE_SPARKS_DISCOVER_URL

BASE_SPARKS_IOCS_URL = '/iocs'
BASE_SPARKS_IOCS_URL = os.getenv('BLUELIV_API_BASE_SPARKS_IOCS_URL',
                                 BASE_SPARKS_IOCS_URL)
# ENV: BLUELIV_API_BASE_SPARKS_IOCS_URL

BASE_IOCS_URL = '/iocs'
BASE_IOCS_URL = os.getenv('BLUELIV_API_BASE_IOCS_URL',
                          BASE_IOCS_URL)
# ENV: BLUELIV_API_BASE_IOCS_URL

BASE_IOCS_TYPES_URL = '/iocs/types'
BASE_IOCS_TYPES_URL = os.getenv('BLUELIV_API_BASE_IOCS_TYPES_URL',
                                BASE_IOCS_TYPES_URL)
# ENV: BLUELIV_API_BASE_IOCS_TYPES_URL

BASE_IOCS_TIMELINE_URL = '/timeline'
BASE_IOCS_TIMELINE_URL = os.getenv('BLUELIV_API_BASE_IOCS_TIMELINE_URL',
                                   BASE_IOCS_TIMELINE_URL)
# ENV: BLUELIV_API_BASE_IOCS_TIMELINE_URL

BASE_IOCS_DISCOVER_URL = '/discover'
BASE_IOCS_DISCOVER_URL = os.getenv('BLUELIV_API_BASE_IOCS_DISCOVER_URL',
                                   BASE_IOCS_DISCOVER_URL)
# ENV: BLUELIV_API_BASE_IOCS_DISCOVER_URL

BASE_TAGS_URL = '/tags'
BASE_TAGS_URL = os.getenv('BLUELIV_API_BASE_TAGS_URL',
                          BASE_TAGS_URL)
# ENV: BLUELIV_API_BASE_TAGS_URL

BASE_TAGS_SPARKS_URL = '/sparks'
BASE_TAGS_SPARKS_URL = os.getenv('BLUELIV_API_BASE_TAGS_SPARKS_URL',
                                 BASE_TAGS_SPARKS_URL)
# ENV: BLUELIV_API_BASE_TAGS_SPARKS_URL

BASE_TAGS_IOCS_URL = '/iocs'
BASE_TAGS_IOCS_URL = os.getenv('BLUELIV_API_BASE_TAGS_IOCS_URL',
                               BASE_TAGS_IOCS_URL)
# ENV: BLUELIV_API_BASE_TAGS_IOCS_URL

BASE_USERS_URL = '/users'
BASE_USERS_URL = os.getenv('BLUELIV_API_BASE_USERS_URL',
                           BASE_USERS_URL)
# ENV: BLUELIV_API_BASE_USERS_URL

BASE_USERS_SPARKS_URL = '/sparks'
BASE_USERS_SPARKS_URL = os.getenv('BLUELIV_API_BASE_USERS_SPARKS_URL',
                                  BASE_USERS_SPARKS_URL)
# ENV: BLUELIV_API_BASE_USERS_SPARKS_URL

BASE_USERS_IOCS_URL = '/iocs'
BASE_USERS_IOCS_URL = os.getenv('BLUELIV_API_BASE_USERS_IOCS_URL',
                                BASE_USERS_IOCS_URL)
# ENV: BLUELIV_API_BASE_USERS_IOCS_URL

BASE_CRAWL_URL = '/crawl'
BASE_CRAWL_URL = os.getenv('BLUELIV_API_BASE_CRAWL_URL',
                           BASE_CRAWL_URL)
# ENV: BLUELIV_API_BASE_CRAWL_URL

BASE_MALWARES_URL = '/malwares'
BASE_MALWARES_URL = os.getenv('BLUELIV_API_BASE_MALWARES_URL',
                              BASE_MALWARES_URL)
# ENV: BLUELIV_API_BASE_MALWARES_URL

BASE_MALWARES_UPLOAD_URL = '/upload'
BASE_MALWARES_UPLOAD_URL = os.getenv('BLUELIV_API_BASE_MALWARES_UPLOAD_URL',
                                     BASE_MALWARES_UPLOAD_URL)
# ENV: BLUELIV_API_BASE_MALWARES_UPLOAD_URL

BASE_SEARCH_URL = '/search'
BASE_SEARCH_URL = os.getenv('BLUELIV_API_BASE_SEARCH_URL',
                            BASE_SEARCH_URL)
# ENV: BLUELIV_API_BASE_SEARCH_URL
