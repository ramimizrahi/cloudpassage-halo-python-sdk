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


class TestIntegrationContainerProcesses:
    def build_container_processes_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        container_processes_object = cloudpassage.ContainerProcesses(session)
        return(container_processes_object)

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        assert cloudpassage.ContainerProcesses(session)

    def test_get_container_processes_list(self):
        """This test requires at least one container process in your Halo
        account.  If you have no container processes, this test will fail.
        """
        c = self.build_container_processes_object()
        container_processes_list = c.list_all()
        assert "id" in container_processes_list[0]

    def test_get_container_processes_details(self):
        """This test requires at least one container process in your Halo
        account.  If you have no container processes, this test will fail.
        """
        c = self.build_container_processes_object()
        container_processes_list = c.list_all()
        assert "id" in container_processes_list[0]

        container_id = container_processes_list[0]["container_id"]
        process = c.describe(container_id)
        assert process["processes"][0]["container_id"] == container_id
