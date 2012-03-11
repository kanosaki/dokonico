import os.path

from nose.tools import *

import dokonico.core as core


APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../etc"))

class TestConfig:
    @property
    def config_path(self):
        return os.path.join(APP_ROOT, "config.json")

    def test_accessor(self):
        config = core.Config(self.config_path)
        assert_equals(config.custom_server["host"], "example.com")

        
