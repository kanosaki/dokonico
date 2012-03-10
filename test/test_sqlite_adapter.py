
import dokonico.browser.sqlite_adapter as sqa
from nose.tools import *

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


        


        
        
