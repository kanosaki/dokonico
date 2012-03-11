
import dokonico.browser.sqlite_adapter

class Browser:
    def __init__(self):
        raise Exception("dokonico.browser.common.Browser is Abstract class")

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
        if len(sessions) == 1:
            return sessions[0]
        else:
            return None


class BrowserFactory:
    def create(self, env):
        if env.name == "Windows":
            return self.windows()
        elif env.name == "Wac":
            return self.mac()
        else:
            raise Exception("Sorry, OS '{0}' is not supported.".format(name))

        
