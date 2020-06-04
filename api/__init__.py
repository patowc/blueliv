"""
API classes and invocation methods are defined withing this package files.

Modules:
    configuration.py: where we set configuration variables (settings). All
    values will have a default, configured for the project, and a value that
    will be extracted from the environment, if the environment variable does
    exist. If does not exist, it will fall on the default.

    core.py: where base classes and methods are defined. Not to be used in a
    direct way if you don't want to deal with raw details and queries.

    crawl.py: module to use Blueliv API capabilities to crawl information on
    IoCs, Sparks and any interesting information related.

    iocs.py: module to search, discover and get details about IoCs.

    malwares.py: module to search, discover and get details on malware samples

    sparks.py: module to search, discover and even publish spark details.

    tags.py: module to search by tag.

    users.py: to retrieve user information.
"""
