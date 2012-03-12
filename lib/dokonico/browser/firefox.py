

import dokonico.core
import dokonico.browser.common

class Firefox(dokonico.browser.common.Browser):
    name = "Firefox"
    def query_session(self):
        with self.adapter as a:
            sessions = a.query()
            return [ FirefoxCookie(s, self) for s in sessions ]


class FirefoxFactory(dokonico.browser.common.BrowserFactory):
    def windows(self):
        return FirefoxWin()

    def mac(self):
        return FirefoxMac()

class FirefoxWin(Firefox):
    pass

class FirefoxMac(Firefox):
    pass

class FirefoxCookie(dokonico.core.Cookie):
    def __init__(self, dic, browser):
        self.browser_name = browser.name
        self.dic = dic
        
    @property
    def time_comparator(self):
        return int(self.creation_utc) / 1000000

