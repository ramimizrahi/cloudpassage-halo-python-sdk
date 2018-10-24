import cloudpassage
import datetime
import json
import os
import re

utility = cloudpassage.utility.Utility
policy_file_name = "firewall.json"
config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)
policy_path = os.path.join(tests_dir, 'policies/')
fw_policy_file = os.path.join(policy_path, policy_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname


class TestUnitUtility:
    def test_merge_dicts(self):
        one = {"a": "Alpha",
               "b": "Bravo",
               "c": "Charlie"}
        two = {"c": "CharlieHorse",
               "d": "Delta",
               "e": "Echo"}
        merge_one = utility.merge_dicts(one, two)
        merge_two = utility.merge_dicts(two, one)
        assert merge_one["c"] == "CharlieHorse"
        assert merge_two["c"] == "Charlie"

    def test_policy_to_dict(self):
        with open(fw_policy_file, 'r') as f:
            policy_string = f.read().replace('\n', '')
        pol_dict = utility.policy_to_dict(policy_string)
        assert type(pol_dict) is dict
        pol_double_dict = utility.policy_to_dict(pol_dict)
        assert pol_double_dict == pol_dict

    def test_parse_status200(self):
        resp_text = "Test text, yo."
        url = "https://whatever.because.none/its-not-critical"
        code_exc = {200: None,
                    201: None,
                    202: None,
                    204: None,
                    400: cloudpassage.CloudPassageValidation(resp_text),
                    401: cloudpassage.CloudPassageAuthentication(resp_text),
                    403: cloudpassage.CloudPassageAuthorization(resp_text),
                    404: cloudpassage.CloudPassageResourceExistence(resp_text),
                    422: cloudpassage.CloudPassageValidation(resp_text),
                    999999: cloudpassage.CloudPassageGeneral(resp_text)}
        code_succ = {200: True,
                     201: True,
                     202: True,
                     204: True,
                     400: False,
                     401: False,
                     403: False,
                     404: False,
                     422: False,
                     "ARBLEGARBLE": False}
        for r, o in code_exc.items():
            success, exc = utility.parse_status(url, r, resp_text)
            assert type(o) == type(exc)
        for r, o in code_succ.items():
            success, exc = utility.parse_status(url, r, resp_text)
            assert success == o

    def test_verify_pages(self):
        assert utility.verify_pages("cats")[0] is False
        assert utility.verify_pages(301)[0] is False

    def test_sanitize_url_params(self):
        params = {"states": ["deactivated", "missing"],
                  "the_best_time": datetime.datetime.utcnow()}
        desired_states = "deactivated,missing"
        actual_result = utility.sanitize_url_params(params)
        assert actual_result["states"] == desired_states
        assert type(actual_result["the_best_time"]) is str

    def test_determine_policy_metadata(self):
        test_csm_lin = {"file": str(policy_path +
                        "/cis-benchmark-for-centos-7-v1.policy.json"),
                        "type": "CSM",
                        "platform": "Linux"}
        test_fim_lin = {"file": str(policy_path +
                        "/core-system-files-centos-v1.fim.json"),
                        "type": "FIM",
                        "platform": "Linux"}
        test_lids_lin = {"file": str(policy_path +
                         "/core-system-centos-v1-1.lids.json"),
                         "type": "LIDS",
                         "platform": "Linux"}
        test_firewall_lin = {"file": str(policy_path +
                             "/firewall.json"),
                             "type": "Firewall",
                             "platform": "Linux"}
        for policy in [test_csm_lin,
                       test_fim_lin,
                       test_lids_lin,
                       test_firewall_lin]:
            with open(policy["file"], 'r') as f:
                policy_string = f.read()
                policy_json = json.loads(policy_string)
            meta_from_str = utility.determine_policy_metadata(policy_string)
            meta_from_json = utility.determine_policy_metadata(policy_json)
            assert meta_from_str == meta_from_json
            assert meta_from_str["policy_type"] == policy["type"]
            assert meta_from_str["target_platform"] == policy["platform"]

    def test_bad_policy_type(self):
        bad_policy_type = ["nope_policy"]
        result = utility.determine_policy_metadata(bad_policy_type)
        assert result["policy_type"] is None

    def test_time_string_now(self):
        assert type(utility.time_string_now()) is str

    def test_assemble_search_criteria(self):
        valid_search_fields = ["something", "something_else"]
        input_search_criteria = {"something": "that thing over there",
                                 "cats": "Do not belong here"}
        result = utility.assemble_search_criteria(valid_search_fields,
                                                  input_search_criteria)
        assert "something" in result
        assert "cats" not in result

    def test_verify_python_version_pass_v2(self):
        actual = "2.7.99"
        target = {"2": "2.7.10", "3": "3.7.0"}
        assert utility.verify_python_version(actual, target)

    def test_verify_python_version_pass_v37(self):
        actual = "3.7.0"
        target = {"2": "2.7.10", "3": "3.7.0"}
        assert utility.verify_python_version(actual, target)

    def test_verify_python_version_fail(self):
        actual = "2.4.9"
        target = {"2": "2.7.10", "3": "3.7.0"}
        assert not utility.verify_python_version(actual, target)

    def test_verify_python_version_fail_31(self):
        actual = "3.1.0"
        target = {"2": "2.7.10", "3": "3.7.0"}
        assert not utility.verify_python_version(actual, target)

    def test_verify_python_version_fail_v1(self):
        actual = "1.0"
        target = {"2": "2.7.10", "3": "3.7.0"}
        assert not utility.verify_python_version(actual, target)

    def test_get_installed_python_version(self):
        rx = re.compile(r'^\d+\.\d+\.\d+$')
        assert rx.match(utility.get_installed_python_version())

    def test_get_sdk_version(self):
        version = utility.get_sdk_version()
        rx = re.compile(r'^\S+\.\S+')
        assert rx.match(version)
