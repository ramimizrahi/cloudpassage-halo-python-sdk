"""Container events class"""

from cloudpassage.http_helper import HttpHelper


class ContainerEvents(object):
    """Initializing the Container Events class:

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
        """Returns a list of all container events.
        This query is limited to 50 pages of 100 items,
        totalling 5000 container events.

        Returns:
            list: List of dictionary objects describing container events
        """

        endpoint = "/v1/container_events"
        key = "container_events"
        max_pages = 50
        request = HttpHelper(self.session)
        response = request.get_paginated(endpoint, key, max_pages)
        return response

    def describe(self, container_id):
        """Get container event details by container ID

        Args:
            id (str): container_id

        Returns:
            dict: Dictionary object describing container event
        """

        endpoint = "/v1/container_events?id=%s" % (container_id)
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        return response
