import json
from .. import configuration
from .core import BASEModel, BluelivRequest


class BluelivUser(BASEModel):
    user_id = None
    username = None
    first_name = None
    last_name = None
    karma = None
    badge = None

    def __init__(self, *args, **kwargs):
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
    _base_url = '/users'
    _users_sparks_url = '/sparks'
    _users_iocs_url = '/iocs'
    username = None
    limit = None
    since_id = None

    def __init__(self, *args, **kwargs):
        if 'token' in kwargs:
            self._custom_token = kwargs.get('token', None)

        if 'base_url' in kwargs:
            self._base_url = kwargs.get('base_url', '/users')
        else:
            self._base_url = configuration.BASE_USERS_URL

        if 'sparks' in kwargs:
            self._users_sparks_url = kwargs.get('sparks', '/sparks')
        else:
            self._users_sparks_url = configuration.BASE_USERS_SPARKS_URL

        if 'iocs' in kwargs:
            self._users_iocs_url = kwargs.get('iocs', '/iocs')
        else:
            self._users_iocs_url = configuration.BASE_USERS_IOCS_URL

        if 'username' in kwargs:
            self.username = kwargs.get('username', None)

        if 'limit' in kwargs:
            self.limit = kwargs.get('limit', None)

        if 'since_id' in kwargs:
            self.since_id = kwargs.get('since_id', None)

        super().__init__(token=self._custom_token)

    def me(self):
        resource = '%s/me' % self._base_url
        results = self.request(resource=resource)
        return results

    def list_sparks(self, username, limit=None, since_id=None):
        params = {}
        resource_url = '%s/%s%s' % (self._base_url,
                                    username,
                                    self._users_sparks_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        results = self.request(resource=resource_url,
                               params=params)

        return results

    def list_iocs(self, username, limit=None, since_id=None):
        params = {}
        resource_url = '%s/%s%s' % (self._base_url,
                                    username,
                                    self._users_iocs_url)

        if since_id:
            params['since_id'] = since_id

        if limit:
            params['limit'] = limit

        results = self.request(resource=resource_url,
                               params=params)

        return results
