import cloudpassage
import datetime
import hashlib
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
bad_key = "abad53c"
proxy_host = '190.109.164.81'
proxy_port = '1080'

# This will make cleaning up easier...
content_prefix = 'SDK_test-'
d_hash = hashlib.md5(datetime.datetime.now().isoformat().encode()).hexdigest()
content_name = (content_prefix + d_hash)


class TestIntegrationHaloSession:
    def create_halo_session_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        return session

    def test_halosession_authentication(self):
        session = self.create_halo_session_object()
        session.authenticate_client()
        assert session.auth_token is not None

    def test_halosession_throws_auth_exception(self):
        session = cloudpassage.HaloSession(bad_key, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        with pytest.raises(cloudpassage.CloudPassageAuthentication) as e:
            session.authenticate_client()
        assert 'Invalid credentials- can not obtain session token.' in str(e)

    def test_halosession_useragent_override(self):
        ua_override = content_prefix
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.authenticate_client()
        session.user_agent = ua_override
        header = session.build_header()
        assert session.user_agent == ua_override
        assert header["User-Agent"] == ua_override

    def test_halosession_build_header(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        session.authenticate_client()
        header = session.build_header()
        assert "Authorization" in header
        assert header["Content-Type"] == "application/json"
