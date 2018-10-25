import cloudpassage
import os
from cloudpassage.utility import Utility as utility

policy_file_name = "firewall.json"
config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)
policy_file = os.path.join(tests_dir, 'policies/', policy_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname
api_port = session_info.api_port


with open(policy_file, 'r') as p_file:
    firewall_policy_body = p_file.read().replace('\n', '')


def create_firewall_policy_object():
    session = cloudpassage.HaloSession(key_id, secret_key,
                                       api_host=api_hostname,
                                       api_port=api_port,
                                       integration_string="SDK-Smoke")
    firewall_policy_object = cloudpassage.FirewallPolicy(session)
    return firewall_policy_object


def create_firewall_rule_object():
    session = cloudpassage.HaloSession(key_id, secret_key,
                                       api_host=api_hostname,
                                       api_port=api_port,
                                       integration_string="SDK-Smoke")
    firewall_rule_object = cloudpassage.FirewallRule(session)
    return firewall_rule_object


def create_firewall_zone_object():
    session = cloudpassage.HaloSession(key_id, secret_key,
                                       api_host=api_hostname,
                                       api_port=api_port,
                                       integration_string="SDK-Smoke")
    firewall_zone_object = cloudpassage.FirewallZone(session)
    return firewall_zone_object


def create_firewall_service_object():
    session = cloudpassage.HaloSession(key_id, secret_key,
                                       api_host=api_hostname,
                                       api_port=api_port,
                                       integration_string="SDK-Smoke")
    firewall_service_object = cloudpassage.FirewallService(session)
    return firewall_service_object


def create_firewall_interface_object():
    session = cloudpassage.HaloSession(key_id, secret_key,
                                       api_host=api_hostname,
                                       api_port=api_port,
                                       integration_string="SDK-Smoke")
    firewall_interface_object = cloudpassage.FirewallInterface(session)
    return firewall_interface_object


def get_target_linux_firewall_policy():
    firewall_policy = create_firewall_policy_object()
    policy_list = firewall_policy.list_all()
    for policy in policy_list:
        if policy["platform"] == 'linux':
            return policy["id"]
    return None


def remove_policy_by_name(policy_name):
    fw_policy_obj = create_firewall_policy_object()
    policy_list = fw_policy_obj.list_all()
    for policy in policy_list:
        if policy["name"] == policy_name:
            fw_policy_obj.delete(policy["id"])


class TestIntegrationFirewallPolicy:

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.FirewallPolicy(session)

    def test_firewall_policy_list_all(self):
        """This test requires that a firewall policy exist in your Halo
        account.  If you don't have a firewall policy in your Halo account,
        this test will fail.
        """
        firewall_policy = create_firewall_policy_object()
        firewall_policy_list = firewall_policy.list_all()
        assert "id" in firewall_policy_list[0]

    def test_firewall_policy_describe(self):
        """This test requires that a firewall policy exist in your Halo
        account.  If you don't have a firewall policy in your Halo account,
        this test will fail.
        """
        firewall_policy = create_firewall_policy_object()
        firewall_policy_list = firewall_policy.list_all()
        target_firewall_policy_id = firewall_policy_list[0]["id"]
        target_policy = firewall_policy.describe(target_firewall_policy_id)
        assert "id" in target_policy

    def test_firewall_policy_create_update_delete(self):
        firewall_policy = create_firewall_policy_object()
        pol_meta = utility.determine_policy_metadata(
            firewall_policy_body)
        remove_policy_by_name(pol_meta["policy_name"])
        remove_policy_by_name("NewName")
        new_policy_id = firewall_policy.create(firewall_policy_body)
        policy_update = {"firewall_policy": {"name": "NewName",
                                             "id": new_policy_id}}
        firewall_policy.update(policy_update)
        delete_error = firewall_policy.delete(new_policy_id)
        assert delete_error is None


class TestIntegrationFirewallRule:
    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.FirewallRule(session)

    def test_list_firewall_policy_rules(self):
        firewall_rule = create_firewall_rule_object()
        target_firewall_policy_id = get_target_linux_firewall_policy()
        policy_rules = firewall_rule.list_all(target_firewall_policy_id)
        assert "id" in policy_rules[0]

    def test_get_firewall_policy_rule_describe(self):
        firewall_rule = create_firewall_rule_object()
        target_firewall_policy_id = get_target_linux_firewall_policy()
        policy_rules = firewall_rule.list_all(target_firewall_policy_id)
        target_rule_id = policy_rules[0]["id"]
        rule_details = firewall_rule.describe(target_firewall_policy_id,
                                              target_rule_id)
        assert "id" in rule_details

    def test_firewall_policy_rule_create_mod_delete(self):
        modification_body = {"firewall_rule": {
                             "comment": "Your momma makes firewall rules"}}
        firewall_policy = create_firewall_policy_object()
        firewall_rule = create_firewall_rule_object()
        target_policy_id = firewall_policy.create(firewall_policy_body)
        rule_imported = firewall_rule.list_all(target_policy_id)[0]
        del rule_imported["url"]
        rule_imported["position"] = 1
        rule_body = {"firewall_rule": rule_imported}
        print(rule_body)
        target_rule_id = firewall_rule.create(target_policy_id, rule_body)
        modification_error = firewall_rule.update(target_policy_id,
                                                  target_rule_id,
                                                  modification_body)
        delete_rule_error = firewall_rule.delete(target_policy_id,
                                                 target_rule_id)
        delete_policy_error = firewall_policy.delete(target_policy_id)
        assert modification_error is None
        assert delete_rule_error is None
        assert delete_policy_error is None


class TestIntegraationFirewallZone:
    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.FirewallZone(session)

    def test_list_all_ip_zones(self):
        firewall_zone = create_firewall_zone_object()
        list_of_zones = firewall_zone.list_all()
        assert "id" in list_of_zones[0]

    def test_get_zone_details(self):
        firewall_zone = create_firewall_zone_object()
        target_zone_id = firewall_zone.list_all()[0]["id"]
        details = firewall_zone.describe(target_zone_id)
        assert "id" in details

    def test_firewall_zone_create_update_delete(self):
        firewall_zone = create_firewall_zone_object()
        firewall_zone_body = {"firewall_zone": {"name": "CPAPI TEST",
                                                "ip_address": "127.0.0.1"}}
        target_zone_id = firewall_zone.create(firewall_zone_body)
        zone_update = {"firewall_zone": {"name": "NewName",
                                         "id": target_zone_id}}
        firewall_zone.update(zone_update)
        delete_error = firewall_zone.delete(target_zone_id)
        assert delete_error is None


class TestIntegrationFirewallService:
    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.FirewallService(session)

    def test_list_all_services(self):
        firewall_service = create_firewall_service_object()
        list_of_services = firewall_service.list_all()
        assert "id" in list_of_services[0]

    def test_get_service_details(self):
        firewall_service = create_firewall_service_object()
        target_service_id = firewall_service.list_all()[0]["id"]
        details = firewall_service.describe(target_service_id)
        assert "id" in details

    def test_firewall_zone_create_update_delete(self):
        firewall_service = create_firewall_service_object()
        firewall_service_body = {"firewall_service": {"name": "CPAPI TEST",
                                                      "protocol": "TCP",
                                                      "port": "1234"}}
        target_service_id = firewall_service.create(firewall_service_body)
        service_update = {"firewall_service": {"name": "NewName",
                                               "id": target_service_id}}
        firewall_service.update(service_update)
        delete_error = firewall_service.delete(target_service_id)
        assert delete_error is None


class TestIntegrationFirewallInterface:
    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.FirewallInterface(session)

    def test_list_all_interfaces(self):
        interface = create_firewall_interface_object()
        list_of_interfaces = interface.list_all()
        assert "id" in list_of_interfaces[0]

    def test_get_interface_details(self):
        interface = create_firewall_interface_object()
        target_interface_id = interface.list_all()[0]["id"]
        details = interface.describe(target_interface_id)
        assert "id" in details

    def test_firewall_interface_create_delete(self):
        interface = create_firewall_interface_object()
        interface_body = {"firewall_interface": {"name": "eth12"}}
        target_interface_id = interface.create(interface_body)
        delete_error = interface.delete(target_interface_id)
        assert delete_error is None
