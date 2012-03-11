
import dokonico.browser.sqlite_adapter as sqlite_adapter

class Browser:
    def __init__(self):
        raise Exception("dokonico.browser.common.Browser is Abstract class")

    @property
    def adapter(self):
        try:
            return self._adapter
        except AttributeError:
            path = self.cookie_db_file
            self._adapter = sqlite_adapter.SQLiteaAdapter(path, self.name)
            return self._adapter

    def session(self):
        sessions = self.query_session()
        if len(sessions) == 1:
            return sessions[0]
        else:
            return None


class BrowserFactory:
    def create(self, name):
        if name == "windows":
            return self.windows()
        elif name == "mac":
            return self.mac()
        else:
            raise Exception("Sorry, OS '{0}' is not supported.".format(name))

        
