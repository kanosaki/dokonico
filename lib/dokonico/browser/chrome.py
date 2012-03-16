
import os
import sqlite3
import time

import dokonico
import dokonico.core
from dokonico.browser import common

class Chrome(common.Browser):
    name = "Chrome"
    def query_session(self):
        with self.adapter as a:
            sessions = a.query()
            return [ ChromeCookie(s, self.name) for s in sessions ]
    
    def _create_specific_cookie(self, cookie):
        return ChromeCookie.from_common(cookie.to_common())
        

class ChromeFactory(common.BrowserFactory):
    def windows(self):
        return ChromeWin(self.env)

    def mac(self):
        return ChromeMac(self.env)

class ChromeWin(Chrome):
    def __init__(self, env):
        self.env = env
        
    @property
    def cookie_db_file(self):
        return os.path.join(self.env.homedir, "Local\\Google\\Chrome\\User Data\\Default\\Cookies")

class ChromeMac(Chrome):
    def __init__(self, env):
        self.env = env

    @property
    def cookie_db_file(self):
        return os.path.join(self.env.homedir, "Library/Application Support/Google/Chrome/Default/Cookies")

class ChromeCookie(dokonico.core.Cookie):
    def __init__(self, dic, browser):
        self.browser_name = browser
        dokonico.core.Cookie.__init__(self, dic)

    @property
    def last_access_ticks(self):
        return self._convert_timestamp(self.last_access_utc)

    @staticmethod
    def _convert_timestamp(val):
        return (int(val)) - 11644473600000000

    @staticmethod
    def _convert_back_timestamp(val):
        return (val + 11644473600000000) 
        
    def to_common(self):
        ret = self.dic.copy()
        ret["creation_utc"] = ChromeCookie._convert_timestamp(ret["creation_utc"])
        ret["expires_utc"] =  ChromeCookie._convert_timestamp(ret["expires_utc"])
        ret["last_access_utc"] = ChromeCookie._convert_timestamp(ret["last_access_utc"])
        return ret

    @staticmethod
    def from_common(dic):
        d = dic.copy()
        d["creation_utc"] =  ChromeCookie._convert_back_timestamp(d["creation_utc"])
        d["expires_utc"] =  ChromeCookie._convert_back_timestamp(d["expires_utc"])
        d["last_access_utc"] =  ChromeCookie._convert_back_timestamp(d["last_access_utc"])
        return ChromeCookie(d, Chrome.name)
        
