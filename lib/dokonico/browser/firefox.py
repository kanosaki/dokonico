
import glob

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
            return os.path.join(dirs[0], "cookies.sqlite")
        

class FirefoxFactory(common.BrowserFactory):
    def windows(self):
        return FirefoxWin()

    def mac(self):
        return FirefoxMac()

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
        self.dic = dic
        
    @property
    def time_comparator(self):
        return int(self.creation_utc) / 1000000

