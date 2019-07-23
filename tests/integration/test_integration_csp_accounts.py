import cloudpassage
import os

config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname
api_port = session_info.api_port


class TestIntegrationCspAccount:
    def build_csp_account_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        csp_account_object = cloudpassage.CspAccount(session)
        print(key_id)
        return csp_account_object

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        assert cloudpassage.CspAccount(session)

    def test_list_all(self):
        """This test gets a list of CSP Accounts from the Halo API.
        If you have no CSP Accounts in Halo, it will fail
        """
        request = self.build_csp_account_object()
        response = request.list_all()
        assert "id" in response[0]
