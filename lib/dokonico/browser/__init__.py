
class BrowserManager:
    def __init__(self, env, conf):
        self.env = env
        self.conf = conf

    def latest(self):
        sessions_raw = map(lambda b : b.session, self.browsers)
        sessions = list(filter(lambda s : s is not None, sessions_raw))
        if len(sessions) == 0:
            return None
        else:
            sessions.sort(key = lambda s : s.time_comparator, reverse=True)
            return sessions[0]

    def push_all(self, cookie):
        for b in self.browsers:
            b.push(cookie)

    @property
    def browsers(self):
        try:
            return self._browsers
        except AttributeError:
            self._browsers = [ f.create() for f in self.factories() ]
            return self._browsers

    def factories(self):
        from dokonico.browser import chrome
        from dokonico.browser import firefox
        yield chrome.ChromeFactory(self.env)
        yield firefox.FirefoxFactory(self.env)

