import imp
import os
import pytest
import sys

from datetime import datetime, timedelta


module_name = 'cloudpassage'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
cloudpassage = imp.load_module(module_name, fp, pathname, description)


class TestIntegrationTimeSeries(object):
    def get_halo_session(self):
        config_file_name = "portal.yaml.local"
        tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                 "../"))
        config_file = os.path.join(tests_dir, "configs/", config_file_name)
        session_info = cloudpassage.ApiKeyManager(config_file=config_file)
        key_id = session_info.key_id
        secret_key = session_info.secret_key
        api_hostname = session_info.api_hostname
        api_port = session_info.api_port
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        return session

    def test_time_series_iter_items_many_pages(self):
        """Test against events, issues, and scans endpoints."""
        session = self.get_halo_session()
        start_time = cloudpassage.utility.datetime_to_8601((datetime.now() -
                                                            timedelta(7)))
        test_scenarios = [{"start_url": "/v1/events", "item_key": "events"},
                          {"start_url": "/v1/scans", "item_key": "scans"}]
        for scenario in test_scenarios:
            start_url = scenario["start_url"]
            item_key = scenario["item_key"]
            streamer = cloudpassage.TimeSeries(session, start_time,
                                               start_url, item_key)
            item_counter = 0
            item_ids = set([])
            for item in streamer:
                assert "id" in item
                assert item["id"] not in item_ids
                item_ids.add(item["id"])
                item_counter += 1
                if item_counter > 60:
                    break

    def test_time_series_iter_items_many_pages_fail(self):
        """Test failures for bad endpoints."""
        session = self.get_halo_session()
        start_time = cloudpassage.utility.datetime_to_8601((datetime.now() -
                                                            timedelta(7)))
        test_scenarios = [{"start_url": "/v1/eventss", "item_key": "events"},
                          {"start_url": "/v1/issuess", "item_key": "issues"},
                          {"start_url": "/v1/scanss", "item_key": "scans"}]
        for scenario in test_scenarios:
            start_url = scenario["start_url"]
            item_key = scenario["item_key"]
            with pytest.raises(cloudpassage.ValidationError):
                streamer = cloudpassage.TimeSeries(session, start_time,
                                                   start_url, item_key)
                assert False  # Break if exception is not caught.
