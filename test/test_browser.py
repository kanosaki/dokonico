
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

CHROME_SAMPLE_DIC = { 
        "creation_utc" : 12345,
        "host_key" : ".example.com",
        "name" : "foobar",
        "value" : "homuhomu",
        "path" : "/",
        "expires_utc" : 6789,
        "is_secure" : 0,
        "is_http_only" : 0,
        "last_access_utc" : 123456,
        "has_expires" : 1,
        "persistent" : 1}

FIREFOX_SAMPLE_DIC = {
        "id" : 451,
        "base_domain" : "nicovideo.jp",
        "name" : "user_session",
        "value" : "homuhomu",
        "host_key" : ".nicovideo.jp",
        "path" : "/",
        "expires_utc" : 1333643758,
        "last_access_utc" : 1331055863395830, 
        "creation_utc" : 1331051758333005,
        "is_secure" : 0,
        "is_http_only" : 0}

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

    def sample_cookie_firefox(self):
        return ff.FirefoxCookie(FIREFOX_SAMPLE_DIC, "Firefox")

    def test_push(self):
        browser = self.browser()
        prev = browser.pull()
        cookie = self.sample_cookie_firefox()
        browser.push(cookie, force=True)
        after = browser.pull()
        assert_not_equals(prev.value, after.value)
        assert_equals(after.value, "homuhomu")

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

    def sample_cookie_firefox(self):
        return ff.FirefoxCookie(FIREFOX_SAMPLE_DIC)
    
        
        
    def test_pull_fail(self):
        browser = self.browser()
        session = browser.pull()
        ok_(session is None)




