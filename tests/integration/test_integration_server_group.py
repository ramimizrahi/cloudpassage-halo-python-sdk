import cloudpassage
import json
import os
import pytest

config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname


class TestIntegrationServerGroup:
    def create_server_group_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return(cloudpassage.ServerGroup(session))

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.ServerGroup(session)

    def test_list_all(self):
        s_grp = self.create_server_group_object()
        groups = s_grp.list_all()
        assert "id" in groups[0]

    def test_describe(self):
        s_grp = self.create_server_group_object()
        groups = s_grp.list_all()
        target_group_id = groups[0]["id"]
        target_group_object = s_grp.describe(target_group_id)
        assert "id" in target_group_object

    def test_list_members(self):
        # Rolls through all server groups, confirms active server IDs
        confirmed = False
        s_grp = self.create_server_group_object()
        groups = s_grp.list_all()
        num_members = 0
        for g in groups:
            target_group_id = g["id"]
            num_members = g["server_counts"]["active"]
            if num_members > 0:
                members = s_grp.list_members(target_group_id)
                assert members[0]["id"]
                confirmed = True
        # Confirm that we actually have a populated server group
        assert confirmed

    def test_create_update_delete_server_group(self):
        update_name = "WHATS_YOUR_TWENTY"
        s_grp = self.create_server_group_object()
        new_grp_id = s_grp.create("TEN_FOUR_GOOD_BUDDY")
        s_grp.update(new_grp_id, name=update_name)
        delete_return = s_grp.delete(new_grp_id)
        assert delete_return is None
