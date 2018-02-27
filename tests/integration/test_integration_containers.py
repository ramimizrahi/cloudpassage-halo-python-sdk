import cloudpassage
import os
import pytest


config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname
api_port = session_info.api_port


class TestIntegrationContainers:
    def build_containers_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        containers_object = cloudpassage.Containers(session)
        return(containers_object)

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        assert cloudpassage.Containers(session)

    def test_get_containers_list(self):
        """This test requires at least one container in your Halo
        account.  If you have no containers, this test will fail.
        """
        c = self.build_containers_object()
        containers_list = c.list_all()
        assert "id" in containers_list[0]

    def test_get_container_details(self):
        """This test requires at least one container in your Halo
        account.  If you have no containers, this test will fail.
        """
        c = self.build_containers_object()
        containers_list = c.list_all()
        assert "id" in containers_list[0]

        target_container_id = containers_list[0]["id"]
        container_details = c.describe(target_container_id)
        assert container_details["id"] == target_container_id

    def test_get_container_details_404(self):
        request = self.build_containers_object()
        bad_container_id = "123456789"
        with pytest.raises(cloudpassage.CloudPassageResourceExistence) as e:
            request.describe(bad_container_id)
        assert "Container not found" in str(e)
