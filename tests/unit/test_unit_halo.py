import cloudpassage
import os
import re


config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname
bad_key = "abad53c"
proxy_host = '190.109.164.81'
proxy_port = '1080'


class TestUnitHaloSession:
    def create_halo_session_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return session

    def test_halosession_christmas_tree(self):
        fake_api = "api.doodles.cloudpassage.com"
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           proxy_ip="10.0.0.1",
                                           proxy_port="8081",
                                           user_agent="SDK TEST",
                                           api_host=fake_api,
                                           api_port=443)
        assert session

    def test_override_useragent_string(self):
        override_string = "Halo API SDK TEST SUITE"
        session = self.create_halo_session_object()
        session.user_agent = override_string
        assert session.user_agent == override_string

    def test_integration_string(self):
        override_string = "Halo API SDK TEST SUITE"
        session = cloudpassage.HaloSession("", "",
                                           integration_string=override_string)
        assert override_string in session.user_agent

    def test_integration_string_2(self):
        int_string = "integration/v1.0"
        ua_string = "sdk/v1.1"
        session = cloudpassage.HaloSession("", "",
                                           integration_string=int_string,
                                           user_agent=ua_string)
        desired = "%s %s" % (int_string, ua_string)
        assert desired == session.user_agent

    def test_integration_string_3(self):
        int_string = "integration/1.0"
        session = cloudpassage.HaloSession("", "",
                                           integration_string=int_string)
        match_rx = "^%s\\s[^/]+/\\d+" % int_string
        assert re.match(match_rx, session.user_agent)

    def test_build_proxy_struct_ip_only(self):
        proxy_ip = "10.0.0.1"
        session = self.create_halo_session_object()
        result = session.build_proxy_struct(proxy_ip, None)
        assert result["https"] == "http://10.0.0.1:8080"

    def test_build_proxy_struct_ip_and_port(self):
        proxy_ip = "10.0.0.1"
        proxy_port = 8081
        session = self.create_halo_session_object()
        result = session.build_proxy_struct(proxy_ip, proxy_port)
        assert result["https"] == "http://10.0.0.1:8081"

    def test_halosession_instantiation(self):
        session = self.create_halo_session_object()
        assert session

    def test_halosession_build_endpoint_prefix(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        default_good = "https://api.cloudpassage.com:443"
        fn_out = session.build_endpoint_prefix()
        assert fn_out == default_good

    def test_halosession_build_endpoint_prefix_fail(self):
        rejected = False
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.api_host = "apples.nonexist.nope.nada"
        try:
            session.build_endpoint_prefix()
        except cloudpassage.CloudPassageValidation:
            rejected = True
        assert rejected

    def test_halosession_with_proxy(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           proxy_host=proxy_host,
                                           proxy_port=proxy_port)
        assert ((session.proxy_host == proxy_host) and
                (session.proxy_port == proxy_port))
