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


class TestIntegrationContainerEvents:
    def build_container_events_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        container_events_object = cloudpassage.ContainerEvents(session)
        return(container_events_object)

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        assert cloudpassage.ContainerEvents(session)

    def test_get_container_events_list(self):
        """This test requires at least one container event in your Halo
        account.  If you have no container events, this test will fail.
        """
        c = self.build_container_events_object()
        container_events_list = c.list_all()
        assert "id" in container_events_list[0]

    def test_get_container_event_details(self):
        """This test requires at least one container event in your Halo
        account.  If you have no container events, this test will fail.
        """
        c = self.build_container_events_object()
        container_events_list = c.list_all()
        assert "id" in container_events_list[0]

        container_event_id = container_events_list[0]["id"]
        container_event = c.describe(container_event_id)
        assert container_event["container_event"]["id"] == container_event_id
