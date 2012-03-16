
import sqlite3
import logging as log

import dokonico.browser.sqlite_adapter



class SessionNotFoundError(Exception):
    pass

class Browser:
    def __init__(self):
        raise Exception("dokonico.browser.common.Browser is Abstract class")

    def push(self, cookie):
        if cookie.browser_name == self.name:
            return
        try:
            s_cookie = self._create_specific_cookie(cookie)
            self.adapter.update(s_cookie.dic)
        except (sqlite3.Error, Exception) as e:
            log.warn(e)
            self.adapter.insert(s_cookie.dic)

    @property
    def adapter(self):
        try:
            return self._adapter
        except AttributeError:
            path = self.cookie_db_file
            self._adapter = dokonico.browser.sqlite_adapter.SQLiteAdapter(path, self.name)
            return self._adapter

    def session(self):
        sessions = self.query_session()
        try:
            return sessions[0]
        except (IndexError, SessionNotFoundError):
            return None

class BrowserFactory:
    def __init__(self, env):
        self.env = env

    def create(self):
        if self.env.name == "Windows":
            return self.windows()
        elif self.env.name == "Mac":
            return self.mac()
        else:
            raise Exception("Sorry, OS '{0}' is not supported.".format(self.env.name))

        
