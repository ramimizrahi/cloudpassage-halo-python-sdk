import cloudpassage
import os

config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname


class TestUnitScan:
    def test_instantiation(self):
        assert cloudpassage.Scan(None)

    def test_scan_type_valid(self):
        valid_types = ["svm", "sva", "csm", "sca", "fim", "sam", "sv"]
        invalid_types = ["death_stare", "lids"]
        scanner = cloudpassage.Scan(None)
        for v in valid_types:
            assert scanner.scan_type_supported(v)
        for i in invalid_types:
            assert not scanner.scan_type_supported(i)

    def test_verify_and_build_status_params(self):
        bad_list = ["cats"]
        bad_string = "cats"
        good_list = ["running"]
        good_string = "running"
        bad_statuses = [bad_list, bad_string]
        good_statuses = [good_list, good_string]
        scanner = cloudpassage.Scan(None)
        for status in bad_statuses:
            try:
                accepted = scanner.verify_and_build_status_params(status)
            except cloudpassage.CloudPassageValidation:
                accepted = False
            assert accepted is False
        for status in good_statuses:
            accepted = scanner.verify_and_build_status_params(status)
            assert accepted == status

        def test_verify_and_build_module_params(self):
            bad_list = ["cats"]
            bad_string = "cats"
            good_list = ["sam"]
            good_string = "sam"
            bad_modules = [bad_list, bad_string]
            good_modules = [good_list, good_string]
            scanner = cloudpassage.Scan(None)
            for status in bad_modules:
                try:
                    accepted = scanner.verify_and_build_module_params(status)
                except cloudpassage.CloudPassageValidation:
                    accepted = False
                assert accepted is False
            for status in good_modules:
                accepted = scanner.verify_and_build_module_params(status)
                assert accepted == status


class TestUnitCveException:
    def test_instantiation(self):
        assert cloudpassage.CveException(None)
