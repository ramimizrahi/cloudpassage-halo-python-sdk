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


class TestIntegrationAgentUpgrade:
    def build_au_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        return(cloudpassage.AgentUpgrade(session))

    def build_server_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        return(cloudpassage.Server(session))

    def test_list_all(self):
        au_obj = self.build_au_object()
        repsonse = au_obj.list_all()
        assert "id" in repsonse[0]

    def test_agent_upgrade_cd(self):
        au_obj = self.build_au_object()
        srv_obj = self.build_server_object()
        target_srvs = srv_obj.list_all()
        target_srv_id = target_srvs[0]["id"]

        body = {
            "id": target_srv_id,
            "agent_version_lt": "latest"
        }

        au_id = au_obj.create(**body)
        delete_return = au_obj.delete(au_id)
        assert delete_return is None
