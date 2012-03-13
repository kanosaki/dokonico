
import os
import warnings

from nose.tools import *

from dokonico.remote import dropbox
from dokonico.browser import firefox

THIS_DIR_PATH = os.path.abspath(os.path.dirname(__file__))
SAMPLE_DUMP = os.path.join(THIS_DIR_PATH, "private/dump.tmp")

SAMPLE_DB = os.path.join(THIS_DIR_PATH, "private/cookies.sqlite")

class DummyFirefox(firefox.Firefox):
    name = "Firefox"
    def __init__(self):
        pass
    @property
    def cookie_db_file(self):
        return SAMPLE_DB

class DummyDropboxConfig:
    def __init__(self):
        pass
        
    session_file_path = SAMPLE_DUMP

class DummyDropbox(dropbox.Dropbox):
    def create_conf(self, env, conf):
        return DummyDropboxConfig()

class TestDropbox:
    def create_dropbox(self):
        return DummyDropbox(None, None)

    def sample_cookie(self):
        ff = DummyFirefox()
        return ff.session()

    def check_files(self):
        p = os.path
        return p.exists(p.dirname(SAMPLE_DUMP)) and \
               p.exists(SAMPLE_DB)

    def test_push_pull(self):
        if not self.check_files():
            warnings.warn("Skipping TestDropbox. Some files and directories were not found")
            return
        d = self.create_dropbox()
        src = self.sample_cookie()
        d.push(src)
        ret = d.pull()
        assert_equals(src.value, ret.value)
        assert_equals(src.browser_name, ret.browser_name)

        
