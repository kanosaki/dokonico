
import sqlite3
import logging as log

import dokonico.browser.sqlite_adapter


class SessionNotFoundError(Exception):
    pass

class Browser:
    def __init__(self):
        raise Exception("dokonico.browser.common.Browser is Abstract class")

    def push(self, cookie, force=False):
        if cookie.identifier == self.pull().identifier and not force:
            return
        del self._session # remove cache
        with self.adapter as a:
            try:
                s_cookie = self._create_specific_cookie(cookie)
                a.update(s_cookie.dic)
            except (sqlite3.Error, Exception) as e:
                log.warn(e)
                a.insert(s_cookie.dic)

    @property
    def adapter(self):
        return dokonico.browser.sqlite_adapter.SQLiteAdapter(self.cookie_db_file, self.name)

    def pull(self):
        try:
            return self._session
        except AttributeError:
            self._update_session()
            return self._session

    def _update_session(self):
        log.debug("Updating session: {}".format(self.name))
        sessions = self.query_session()
        try:
            self._session = sessions[0]
        except (IndexError, SessionNotFoundError):
            self._session = None
        

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
        
