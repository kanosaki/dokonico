
import os
import warnings

from nose.tools import *

import dokonico.browser.sqlite_adapter as sqa

THIS_DIR_PATH = os.path.abspath(os.path.dirname(__file__))

class TestSQLiteAdapter:
    def sample_db(self):
        return os.path.join(THIS_DIR_PATH, "./private/cookies.sqlite")

    def test_lookup(self):
        db_file = self.sample_db()
        if os.path.exists(db_file):
            self.exec_lookup(db_file)
        else:
            warnings.warn("Sample database not found, skipping.")


    def exec_lookup(self, path):
        ret = None
        with sqa.SQLiteAdapter(path, "firefox") as a:
            ret = a.query()
        assert_equals(len(ret), 1)
        row = ret[0]
        assert_equals(row['host_key'], '.nicovideo.jp')
        assert_equals(row['name'], 'user_session')
        assert_equals(row['path'], '/')

class TestNameTable:
    def test_convert_chrome(self):
        factory = sqa.NameTableFactory.default
        chrome_table = factory.create("chrome")

        assert_equals(
            chrome_table.special_name("is_http_only"),
            "httponly"
        )

        assert_equals(
            chrome_table.common_name("httponly"),
            "is_http_only"
        )

    def test_convert_firefox(self):
        factory = sqa.NameTableFactory.default
        firefox_table = factory.create("firefox")

        assert_equals(
            firefox_table.special_name("expires_utc"),
            "expiry"
        )
        assert_equals(
            firefox_table.common_name("expiry"),
            "expires_utc"
        )

    @raises(KeyError)
    def test_undefined_common_column_name(self):
        factory = sqa.NameTableFactory.default
        chrome_table = factory.create("chrome")
        chrome_table.common_name("foobar")

    @raises(ValueError)
    def test_factory_undefined_browser(self):
        factory = sqa.NameTableFactory.default
        factory.create("safari")

    def test_column_number(self):
        factory = sqa.NameTableFactory.default
        table = factory.create("chrome")
        assert_equals(
            table.column_number("creation_utc"), 0         
        )


        


        
        
