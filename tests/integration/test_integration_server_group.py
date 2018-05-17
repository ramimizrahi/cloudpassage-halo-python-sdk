import cloudpassage
import os
import uuid

config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname
api_port = session_info.api_port


class TestIntegrationServerGroup:
    def create_server_group_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        return(cloudpassage.ServerGroup(session))

    def remove_group_by_name(self, group_name):
        server_grp_obj = self.create_server_group_object()
        grp_list = server_grp_obj.list_all()
        for group in grp_list:
            if group["name"] == group_name:
                server_grp_obj.delete(group["id"])

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
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
        random_num = str(uuid.uuid1())
        name = "TEN_FOUR_GOOD_BUDDY -- %s" % random_num
        update_name = "WHATS_YOUR_TWENTY -- %s" % random_num
        s_grp = self.create_server_group_object()
        new_grp_id = s_grp.create(name)
        s_grp.update(new_grp_id, name=update_name)
        delete_return = s_grp.delete(new_grp_id)
        assert delete_return is None

    def test_create_update_child_server_group(self):
        s_grp = self.create_server_group_object()
        random_num = str(uuid.uuid1())
        name = "TEN_FOUR_GOOD_BUDDY -- %s" % random_num
        child_name = "WHATS_YOUR_TWENTY -- %s" % random_num
        parent_id = s_grp.create(name)
        child_id = s_grp.create(child_name, parent_id=parent_id)
        assert parent_id == s_grp.describe(child_id)["parent_id"]

        groups = s_grp.list_all()
        for group in groups:
            if not group["parent_id"]:
                root_id = group['id']
                break

        s_grp.update(child_id, parent_id=root_id)

        assert root_id == s_grp.describe(child_id)["parent_id"]

        delete_child = s_grp.delete(child_id)
        delete_parent = s_grp.delete(parent_id)

        assert delete_child is None
        assert delete_parent is None

    def test_list_connections(self):
        s_grp = self.create_server_group_object()
        groups = s_grp.list_all()
        target_group_id = groups[0]["id"]
        connections = s_grp.list_connections(target_group_id)
        assert isinstance(connections, list)
