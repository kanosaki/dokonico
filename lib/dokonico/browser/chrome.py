
import os

import dokonico
import dokonico.core
from dokonico.browser import common

class Chrome(common.Browser):
    name = "Chrome"
    def query_session(self):
        with self.adapter as a:
            sessions = a.query()
            return [ ChromeCookie(s, self) for s in sessions ]


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
        self.browser_name = browser.name
        self.dic = dic

    @property
    def time_comparator(self):
        return int(self.creation_utc) / 10000000
        
