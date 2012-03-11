
import dokonico
import dokonico.core
from dokonico.browser import common

class Chrome(common.Browser):
    name = "chrome"
    def query_session(self):
        with self.adapter as a:
            sessions = a.query()
            return [ ChromeCookie(s) for s in sessions ]


class ChromeFactory(common.BrowserFactory):
    def windows(self):
        return ChromeWin()

    def mac(self):
        return ChromeMac()

class ChromeWin(Chrome):
    @property
    def cookie_db_file(self):
        return """C:\\<<UserName>>\\Local\\Google\\Chrome\\Default\\User Data\\Cookies"""

class ChromeMac(Chrome):
    @property
    def cookie_db_file(self):
        return """/Users/<<UserName>>/Library/Application Support/Google/Chrome/Default/Cookies"""

class ChromeCookie(dokonico.core.Cookie):
    def __init__(self, dic):
        self.dic = dic
        
