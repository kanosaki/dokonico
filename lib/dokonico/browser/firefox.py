
import glob
import os

import dokonico.core
from dokonico.browser import common

class Firefox(common.Browser):
    name = "Firefox"
    def query_session(self):
        with self.adapter as a:
            sessions = a.query()
            return [ FirefoxCookie(s, self) for s in sessions ]

    @property
    def cookie_db_file(self):
        dirs = glob.glob1(self.profiles_dir, "*.default")
        if len(dirs) == 0:
            raise common.SessionNotFoundError()
        elif len(dirs) > 1:
            raise Exception("There are plural default profile directories in Firefox.")
        else:
            return os.path.join(self.profiles_dir ,dirs[0], "cookies.sqlite")
        
    def _create_specific_cookie(self, cookie):
        return FirefoxCookie.from_common(cookie.to_common())

class FirefoxFactory(common.BrowserFactory):
    def windows(self):
        return FirefoxWin(self.env)

    def mac(self):
        return FirefoxMac(self.env)

class FirefoxWin(Firefox):
    def __init__(self, env):
        self.env = env

    @property
    def profiles_dir(self):
        return os.path.join(self.env.app_data, "Mozilla\\Firefox\\Profiles")

class FirefoxMac(Firefox):
    def __init__(self, env):
        self.env = env

    @property
    def profiles_dir(self):
        return os.path.join(self.env.homedir, "Library/Application Support/Firefox/Profiles")

class FirefoxCookie(dokonico.core.Cookie):
    def __init__(self, dic, browser):
        self.browser_name = browser.name
        dokonico.core.Cookie.__init__(self, dic)
        
    @property
    def last_access_ticks(self):
        return int(self.last_access_utc) / 1000000

    @property
    def expire_ticks(self):
        return int(self.expire_utc)

    def to_common(self):
        ret = self.dic.copy()
        ret["creation_utc"] /= 1000000
        ret["expires_utc"] /= 1000000
        ret["last_access_utc"] /= 1000000
        return ret

    @staticmethod
    def from_common(dic):
        dic["creation_utc"] *= 1000000
        dic["expires_utc"] *= 1000000
        dic["last_access_utc"] *= 1000000
        return ChromeCookie(dic, Chrome.name)
        
