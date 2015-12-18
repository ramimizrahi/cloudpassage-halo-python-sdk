import cloudpassage
import datetime
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


class TestEvent:
    def create_event_obj(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return cloudpassage.Event(session)

    def test_instantiation(self):
        assert self.create_event_obj()

    def test_list_five_pages(self):
        event = self.create_event_obj()
        event_list = event.list_all(5)
        assert "id" in event_list[0]

    def test_too_big(self):
        rejected = False
        event = self.create_event_obj()
        try:
            event.list_all(101)
        except cloudpassage.CloudPassageValidation:
            rejected = True
        assert rejected

    def test_windows(self):
        rejected = False
        event = self.create_event_obj()
        event_list = event.list_all(2, server_platform="windows")
        assert "id" in event_list[0]

    def test_one_day_ago_until_now(self):
        event = self.create_event_obj()
        until = cloudpassage.utility.time_string_now()
        since = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        event_list = event.list_all(10, since=since, until=until)
        assert "id" in event_list[0]
