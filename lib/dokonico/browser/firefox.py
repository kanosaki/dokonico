

import dokonico.core
import dokonico.browser.common

class Firefox(dokonico.browser.common.Browser):
    def query_session(self):
        with self.adapter as a:
            sessions = a.query()
            return [ FirefoxCookie(s) for s in sessions ]


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
    def __init__(self, dic):
        self.dic = dic
        
