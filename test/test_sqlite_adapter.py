
import os
import warnings
import shutil

from nose.tools import *
import nose.tools

import dokonico.browser.sqlite_adapter as sqa

THIS_DIR_PATH = os.path.abspath(os.path.dirname(__file__))

qb_factory = sqa.QueryBuilderFactory(None)
CHROME_SAMPLE_DIC = { 
        "creation_utc" : "12345",
        "host_key" : ".example.com",
        "name" : "foobar",
        "value" : "homuhomu",
        "path" : "/",
        "expires_utc" : "6789",
        "is_secure" : "0",
        "is_http_only" : "0",
        "last_access_utc" : "123456",
        "has_expires" : "1",
        "persistent" : "1"}

FIREFOX_SAMPLE_DIC = {
        "id" : "451",
        "base_domain" : "nicovideo.jp",
        "name" : "user_session",
        "value" : "homuhomu",
        "host_key" : ".nicovideo.jp",
        "path" : "/",
        "expires_utc" : "1333643758",
        "last_access_utc" : "1331055863395830", 
        "creation_utc" : "1331051758333005",
        "is_secure" : "0",
        "is_http_only" : "0"}

class TestSQLiteAdapter:
    def sample_db(self):
        return os.path.join(THIS_DIR_PATH, "./private/cookies.sqlite")

    def sample_db_bak(self):
        return os.path.join(THIS_DIR_PATH, "./private/cookies.sqlite.bak")

    def restore_db(self):
        shutil.copy(self.sample_db_bak(), self.sample_db())

    def teardown(self):
        self.restore_db()

    def test_lookup(self):
        db_file = self.sample_db()
        if os.path.exists(db_file):
            self.exec_lookup(db_file)
        else:
            warnings.warn("Sample database not found, skipping.")

    def exec_lookup(self, path):
        ret = None
        with sqa.SQLiteAdapter(path, "Firefox") as a:
            ret = a.query()
        assert_equals(len(ret), 1)
        row = ret[0]
        assert_equals(row['host_key'], '.nicovideo.jp')
        assert_equals(row['name'], 'user_session')
        assert_equals(row['path'], '/')

    def exec_update(self, db_path):
        with sqa.SQLiteAdapter(db_path, "Firefox") as a:
            before = a.query()[0]
            assert_equals(1331051758414705, before['creation_utc'])
            assert_equals('nicovideo.jp', before['base_domain'])
            assert_equals('.nicovideo.jp', before['host_key'])
            assert_equals('user_session_1138394_2371933031318410806', before['value'])
            a.update(FIREFOX_SAMPLE_DIC)
            after = a.query()[0]
            assert_equals(1331051758333005, after['creation_utc'])
            assert_equals('nicovideo.jp', after['base_domain'])
            assert_equals('.nicovideo.jp', after['host_key'])
            assert_equals('homuhomu', after['value'])

    def test_update(self):
        db_file = self.sample_db()
        if os.path.exists(db_file):
            self.exec_update(db_file)
        else:
            warnings.warn("Sample database not found, skipping.")

    def test_insert(self):
        db_file = self.sample_db()
        if os.path.exists(db_file):
            pass
            #self.exec_update(db_file)
        else:
            warnings.warn("Sample database not found, skipping.")

    def test_insert(self):
        pass


class TestQueryBuilder:
    def test_select(self):
        qb = qb_factory.create("Chrome")
        sql = qb.select()
        expected = "SELECT creation_utc,host_key,name,value,path,expires_utc,secure,httponly,last_access_utc,has_expires,persistent FROM cookies WHERE host_key = '.nicovideo.jp' and name = 'user_session';"
        assert_equals(sql,expected)

    def test_insert(self):
        qb = qb_factory.create("Chrome")
        sql = qb.insert(CHROME_SAMPLE_DIC)
        expected = "INSERT INTO cookies VALUES(12345,'.example.com','foobar','homuhomu','/',6789,0,0,123456,1,1)"
        assert_equals(sql, expected)

    def sample_db(self):
        return os.path.join(THIS_DIR_PATH, "./private/cookies.sqlite")

    def test_insert_firefox(self):
        with sqa.SQLiteAdapter(self.sample_db(), "Firefox") as adapter:
            qb_factory = sqa.QueryBuilderFactory(adapter)
            qb = qb_factory.create("Firefox")
            sql = qb.insert(FIREFOX_SAMPLE_DIC)
            expected = "INSERT INTO moz_cookies VALUES(849,'nicovideo.jp','user_session','homuhomu','.nicovideo.jp','/',1333643758,1331055863395830,1331051758333005,0,0)"
            assert_equals(expected, sql)

    def test_delete_firefox(self):
        qb = qb_factory.create("Firefox")
        sql = qb.delete(FIREFOX_SAMPLE_DIC)
        expected = "DELETE FROM moz_cookies WHERE id=451"
        assert_equals(expected, sql)

    def test_delete_chrome(self):
        qb = qb_factory.create("Chrome")
        sql = qb.delete(CHROME_SAMPLE_DIC)
        expected = "DELETE FROM cookies WHERE host_key='.example.com' and name='foobar'"
        assert_equals(expected, sql)

    def test_update(self):
        qb = qb_factory.create("Chrome")
        sql = qb.update(CHROME_SAMPLE_DIC)
        expected = "UPDATE cookies SET creation_utc=12345,host_key='.example.com',name='foobar',value='homuhomu',path='/',expires_utc=6789,secure=0,httponly=0,last_access_utc=123456,has_expires=1,persistent=1 WHERE host_key = '.nicovideo.jp' and name = 'user_session';"
        assert_equals(sql, expected)
        

nt_factory = sqa.NameTableFactory.default
class TestNameTable:
    def test_convert_chrome(self):
        chrome_table = nt_factory.create("Chrome")

        assert_equals(
            chrome_table.special_name("is_http_only"),
            "httponly"
        )

        assert_equals(
            chrome_table.common_name("httponly"),
            "is_http_only"
        )

    def test_convert_firefox(self):
        firefox_table = nt_factory.create("Firefox")

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
        chrome_table = nt_factory.create("Chrome")
        chrome_table.common_name("foobar")

    @raises(ValueError)
    def test_factory_undefined_browser(self):
        nt_factory.create("safari")

    def test_column_number(self):
        table = nt_factory.create("Chrome")
        assert_equals(
            table.column_number("creation_utc"), 0         
        )

    def test_column_headers_chrome(self):
        chrome = nt_factory.create("Chrome")
        headers = chrome.column_headers
        expected = ["creation_utc", 
                "host_key", "name", 
                "value", "path",
                "expires_utc", "secure",
                "httponly", "last_access_utc",
                "has_expires", "persistent"]
        assert_list_equal(headers, expected)
        
    def test_column_headers_firefox(self):
        firefox = nt_factory.create("Firefox")
        headers = firefox.column_headers
        expected = [
                "id", "baseDomain", "name",
                "value", "host", "path", "expiry", 
                "lastAccessed", "creationTime",
                "isSecure", "isHttpOnly"]
        assert_list_equal(headers, expected)

        
        
        
