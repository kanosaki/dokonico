
import os
import warnings

from nose.tools import *

import dokonico.env
import dokonico.browser.firefox as ff


THIS_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
SAMPLE_DB = os.path.join(THIS_DIR_PATH, "private/cookies.sqlite")

class DummyFirefox(ff.Firefox):
    name = "firefox"
    def __init__(self):
        pass
    @property
    def cookie_db_file(self):
        return SAMPLE_DB
        
class TestBrowser:
    def test_session(self):
        if os.path.exists(SAMPLE_DB):
            self._execute_session(SAMPLE_DB)
        else:
            warnings.warn("Sample database not found. Skipping.")

    def browser(self):
        return DummyFirefox()

    def _execute_session(self, path):
        browser = self.browser()
        session = browser.session()
        assert_equals(session.name, "user_session")
        assert_equals(session.host_key, ".nicovideo.jp")




