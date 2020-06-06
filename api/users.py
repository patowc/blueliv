"""
Module to get information about users, including self.

"""
import typing

from .configuration import (
    BASE_USERS_URL
)

from .core import BASEModel, BluelivRequest


class BluelivUser(BASEModel):  # pylint: disable=too-few-public-methods
    """
    Model to store User details.

    """
    user_id = None
    username = None
    first_name = None
    last_name = None
    karma = None
    badge = None

    def __init__(self, **kwargs):
        if 'user_id' in kwargs:
            self.user_id = kwargs.get('user_id', None)

        if 'username' in kwargs:
            self.username = kwargs.get('username', None)

        if 'first_name' in kwargs:
            self.first_name = kwargs.get('first_name', None)

        if 'last_name' in kwargs:
            self.last_name = kwargs.get('last_name', None)

        if 'karma' in kwargs:
            self.karma = kwargs.get('karma', None)

        if 'badge' in kwargs:
            self.last_name = kwargs.get('badge', None)

        super().__init__()


class UsersRequest(BluelivRequest):
    """
    Model to perfom requests for user information.

    """

    # pylint: disable=too-many-instance-attributes

    _users_sparks_url: str = ''
    _users_iocs_url: str = ''
    username: typing.Optional[str] = None

    def __init__(self, **kwargs):
        self._category = 'users'
        self._base_url = '/users'
        self._users_sparks_url = '/sparks'
        self._users_iocs_url = '/iocs'
        self.username = None
        self.limit = None
        self.since_id = None

        if 'token' in kwargs:
            self._custom_token = kwargs.get('token', None)

        if 'base_url' in kwargs:
            self._base_url = kwargs.get('base_url', '/users')
        else:
            self._base_url = BASE_USERS_URL

        if 'category' in kwargs:
            self._category = kwargs.get('category', 'users')

        if 'username' in kwargs:
            self.username = kwargs.get('username', None)

        if 'limit' in kwargs:
            self.limit = kwargs.get('limit', None)

        if 'since_id' in kwargs:
            self.is_text = kwargs.get('since_id', False)

        super().__init__(token=self._custom_token,
                         base_url=self._base_url,
                         category=self._category,
                         limit=self.limit,
                         since_id=self.since_id)

    def me(self):  # pylint: disable=invalid-name
        """
        Me retrieve information about our own user. The name has a conflict
        with C0103-lint, so we put an exception for pylint and other linters.

        :return: user details as JSON, dict or list.
        """
        resource = '%s/me' % self._base_url
        return self.request(resource=resource)

    def list_sparks(self, username, limit=None, since_id=None):
        """
        List sparks associated with an username.

        :param username: the username to search associated sparks.
        :param limit: the maximum number of items we want to retrieve.
        :param since_id: the reference id from we want to receive items.
        :return: dict, list or JSON with the sparks.

        """
        params = {}
        resource_url = '%s/%s%s' % (self._base_url,
                                    username,
                                    self._users_sparks_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        return self.request(resource=resource_url,
                            params=params)

    def list_iocs(self, username, limit=None, since_id=None):
        """
        List IoCs associated with the user by username.

        :param username: the username.
        :param limit: the maximum number of items we want to retrieve.
        :param since_id: the reference id from we want to receive items.
        :return: dict, list or JSON with the IoCs.

        """
        params = {}
        resource_url = '%s/%s%s' % (self._base_url,
                                    username,
                                    self._users_iocs_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        return self.request(resource=resource_url,
                            params=params)
