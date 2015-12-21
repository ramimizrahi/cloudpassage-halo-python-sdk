'''docstring'''

import re
import cloudpassage.sanity as sanity
import cloudpassage.utility as utility
from cloudpassage.exceptions import CloudPassageValidation
from cloudpassage.http_helper import HttpHelper


class Server(object):
    """Initializing the Server class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    def __init__(self, session):
        self.session = session
        self.valid_server_states = ["active",
                                    "deactivated",
                                    "missing"]
        self.cve_validator = re.compile("^CVE-\d+-\d{4,}$")
        self.kb_validator = re.compile("^kb\d+$")
        self.platform_validator = re.compile("^[a-z]+$")
        self.supported_search_fields = ["state",
                                        "platform",
                                        "cve",
                                        "kb",
                                        "missing_kb"]
        return None

    def list_all(self, **kwargs):
        """Returns a list of all servers.

        This query is limited to 50 pages of 10 items,
        totaling 500 servers.

        Default filter returns only servers in the 'active' state.

        Keyword Args:
            state (list or str): A list or comma-separated string containing \
            any of these: active, missing, deactivated
            platform (list or str): A list or comma-separated string \
            containing any of these: \
            windows, debian, ubuntu, centos, oracle, rhel, etc...
            cve (str): CVE ID.  Example: CVE-2015-1234
            kb (str): Search for presence of KB.  Example: kb="KB2485376"
            missing_kb (str): Search for absence of KB.  \
            Example: mising_kb="KB2485376"

        Returns:
            list: List of dictionary objects describing servers

        """

        endpoint = "/v1/servers"
        request_params_raw = {}
        key = "servers"
        max_pages = 50
        request = HttpHelper(self.session)
        criteria_valid = self.validate_server_search_criteria(kwargs)
        if criteria_valid is False:
            error_text = "Unsupported arguments in " + str(kwargs)
            raise CloudPassageValidation(error_text)
        for param in self.supported_search_fields:
            if param in kwargs:
                request_params_raw[param] = kwargs[param]
        if request_params_raw != {}:
            request_params = utility.sanitize_url_params(request_params_raw)
            response = request.get_paginated(endpoint, key, max_pages,
                                             params=request_params)
        else:
            response = request.get_paginated(endpoint, key, max_pages)
        return response

    def assign_group(self, server_id, group_id):
        """Moves server to another group.

        Args:
            server_id (str): Target server's ID
            group_id (str): ID of group to move server to.

        Returns:
            True if successful, throws exceptions if it fails.

        """

        sanity.validate_object_id(server_id)
        endpoint = "/v1/servers/%s" % server_id
        request_body = {"server": {"group_id": group_id}}
        request = HttpHelper(self.session)
        request.put(endpoint, request_body)
        # Exception will throw if the prior line fails.
        return True

    def delete(self, server_id):
        """Deletes server indicated by server_id.

        Remember, deletion causes the removal of accociated security
        events and scan information.

        Args:
            server_id (str): ID of server to be deleted

        Returns:
            True if successful, throws exceptions otherwise.

        """

        sanity.validate_object_id(server_id)
        endpoint = "/v1/servers/%s" % server_id
        request = HttpHelper(self.session)
        request.delete(endpoint)
        # If no exception from request, we're successful
        return True

    def describe(self, server_id):
        """Get server details by server ID

        Args:
            server_id (str): Server ID

        Returns:
            dict: Dictionary object describing server

        """

        endpoint = "/v1/servers/%s" % server_id
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        server_details = response["server"]
        return server_details

    def retire(self, server_id):
        """This method retires a server

        Args:
            server_id (str): ID of server to be retired

        Returns:
            True if successful, throws exception on failure

        """

        sanity.validate_object_id(server_id)
        endpoint = "/v1/servers/%s" % server_id
        body = {"server":
                {"retire": True}}
        request = HttpHelper(self.session)
        request.put(endpoint, body)
        # Exceptions fire deeper if this fails.  Otherwise, return True.
        return True

    def command_details(self, server_id, command_id):
        """This method retrieves the details and status of a server command.

        Args:
            server_id (str): ID of server runnung command
            command_id (str): ID of command running on server

        Returns:
            dict: Command status as a dictionary object.

        Example:

        ::

            {
              "name": "",
              "status: "",
              "created_at": "",
              "updated_at": "",
              "result": ""
             }


        For server account creation and server account password resets, \
        the password will be contained in the result field, as a dictionary:


        ::

            {
              "name": "",
              "status: "",
              "created_at": "",
              "updated_at": "",
              "result": {
                         "password": ""
                         }
            }


        """

        endpoint = "/v1/servers/%s/commands/%s" % (server_id, command_id)
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        command_status = response["command"]
        return command_status

    # pylint: disable=missing-docstring
    def validate_server_search_criteria(self, criteria):
        arguments_valid = True
        if "state" in criteria:
            if not self.validate_server_state(criteria["state"]):
                arguments_valid = False
        if "platform" in criteria:
            if not self.validate_platform(criteria["platform"]):
                arguments_valid = False
        if "cve" in criteria:
            if not self.validate_cve_id(criteria["cve"]):
                arguments_valid = False
        if "kb" in criteria:
            if not self.validate_kb_id(criteria["kb"]):
                arguments_valid = False
        if "missing_kb" in criteria:
            if not self.validate_kb_id(criteria["missing_kb"]):
                arguments_valid = False
        return arguments_valid

    # pylint: disable=missing-docstring
    def validate_server_state(self, state):
        if isinstance(state, list):
            for s in state:
                if s not in self.valid_server_states:
                    return False
        else:
            if state not in self.valid_server_states:
                return False
        return True

    def validate_platform(self, platform):  # pylint: disable=missing-docstring
        if isinstance(platform, list):
            for p in platform:
                if not self.platform_validator.match(p):
                    return False
        else:
            if not self.platform_validator.match(platform):
                return False
        return True

    def validate_cve_id(self, cve_id):  # pylint: disable=missing-docstring
        if isinstance(cve_id, list):
            for c in cve_id:
                if not self.cve_validator.match(c):
                    return False
        else:
            if not self.cve_validator.match(cve_id):
                return False
        return True

    def validate_kb_id(self, kb_id):  # pylint: disable=missing-docstring
        if isinstance(kb_id, list):
            for k in kb_id:
                if not self.kb_validator.match(k):
                    return False
        else:
            if not self.kb_validator.match(kb_id):
                return False
        return True
