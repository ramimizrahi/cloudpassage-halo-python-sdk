"""Container processes class"""

from cloudpassage.http_helper import HttpHelper


class ContainerProcesses(object):
    """Initializing the Container Processes class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    def __init__(self, session):
        self.session = session
        return None

    def list_all(self, **kwargs):
        """Returns a list of all container processes.
        This query is limited to 50 pages of 100 items,
        totalling 5000 container processes.

        Returns:
            list: List of dictionary objects describing container processes
        """

        endpoint = "/v1/container_processes"
        key = "processes"
        max_pages = 50
        request = HttpHelper(self.session)
        response = request.get_paginated(endpoint, key, max_pages)
        return response

    def describe(self, container_id):
        """Get container processes details by container ID

        Args:
            id (str): container_id

        Returns:
            dict: Dictionary object describing container processes
        """

        endpoint = "/v1/container_processes?container_id=%s" % (container_id)
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        return response
