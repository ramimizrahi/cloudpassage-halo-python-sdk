"""CspFinding class"""

from .halo_endpoint import HaloEndpoint
import cloudpassage.sanity as sanity


class CspFinding(HaloEndpoint):
    """Initializing the CspAccount class:

    Args:
        session (:class:`cloudpassage.HaloSession`): This will define how you
            interact with the Halo API, including proxy settings and API keys
            used for authentication.

    Keyword args:
        endpoint_version (int): Endpoint version override.

    """

    object_name = "csp_finding"
    objects_name = "csp_findings"
    default_endpoint_version = 1

    def endpoint(self):
        """Return endpoint for API requests."""
        return "/v{}/{}".format(self.endpoint_version, self.objects_name)

    def pagination_key(self):
        """Return the pagination key for parsing paged results."""
        return self.objects_name

    def object_key(self):
        """Return the object key for parsing detailed results."""
        return self.object_name

    def describe(self, rule_id):
        """Get all detailed CSP finding results for each rule

        Args:
            rule_id (str): The UUID number of the rule that was applied

        Returns:
            list: List of dictionaries of all CSP finding
            results for the specific rule_id

        """

        sanity.validate_object_id(rule_id)
        return self.list_all(rule_id=rule_id)

    def create(self):
        """Not implemented for this object."""
        raise NotImplementedError

    def delete(self):
        """Not implemented for this object."""
        raise NotImplementedError

    def update(self):
        """Not implemented for this object."""
        raise NotImplementedError
