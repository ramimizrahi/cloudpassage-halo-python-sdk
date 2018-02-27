"""Container class"""

from cloudpassage.http_helper import HttpHelper


class Containers(object):
    """Initializing the Containers class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    def __init__(self, session):
        self.session = session
        return None

    def list_all(self):
        """Returns a list of all connections.

        This query is limited to 50 pages of 100 items,
        totalling 5000 containers.

        Returns:
            list: List of dictionary objects describing containers

        """

        endpoint = "/v1/containers?per_page=100"
        key = "containers"
        max_pages = 50
        request = HttpHelper(self.session)
        response = request.get_paginated(endpoint, key, max_pages)
        return response

    def describe(self, container_id):
        """Get container details by container ID

        Args:
            id (str): container ID

        Returns:
            dict: Dictionary object describing container

        """

        endpoint = "/v1/containers/%s" % container_id
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        container_details = response["container"]
        return container_details
