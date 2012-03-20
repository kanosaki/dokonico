
import os
import warnings
import shutil

from nose.tools import *

import dokonico.env
import dokonico.browser.firefox as ff


THIS_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
SAMPLE_DB = os.path.join(THIS_DIR_PATH, "private/cookies.sqlite")
SAMPLE_DB_BAK = os.path.join(THIS_DIR_PATH, "private/cookies.sqlite.bak")
SAMPLE_DB_VACANT = os.path.join(THIS_DIR_PATH, "private/cookies_vac.sqlite")
SAMPLE_DB_VACANT_BAK = os.path.join(THIS_DIR_PATH, "private/cookies_vac.sqlite.bak")

class DummyFirefox(ff.Firefox):
    name = "Firefox"
    def __init__(self, db):
        self._cookie_db_file = db

    @property
    def cookie_db_file(self):
        return self._cookie_db_file
        
class TestBrowser:
    def test_session(self):
        if os.path.exists(SAMPLE_DB):
            self._execute_session(SAMPLE_DB)
        else:
            warnings.warn("Sample database not found. Skipping.")

    def sample_db(self):
        return SAMPLE_DB

    def sample_db_bak(self):
        return SAMPLE_DB_BAK

    def restore_db(self):
        shutil.copy(self.sample_db_bak(), self.sample_db())

    def teardown(self):
        self.restore_db()

    def browser(self):
        try:
            return self._browser
        except AttributeError:
            self._browser = DummyFirefox(self.sample_db())
            return self._browser

    def _execute_session(self, path):
        browser = self.browser()
        session = browser.pull()
        assert_equals(session.name, "user_session")
        assert_equals(session.host_key, ".nicovideo.jp")

class TestBrowserEx:
    def sample_db(self):
        return SAMPLE_DB_VACANT

    def sample_db_bak(self):
        return SAMPLE_DB_VACANT_BAK

    def restore_db(self):
        shutil.copy(self.sample_db_bak(), self.sample_db())

    def teardown(self):
        self.restore_db()

    def browser(self):
        try:
            return self._browser
        except AttributeError:
            self._browser = DummyFirefox(self.sample_db())
            return self._browser
        
    def test_pull_fail(self):
        browser = self.browser()
        session = browser.pull()
        ok_(session is None)




