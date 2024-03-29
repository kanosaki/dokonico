
class BrowserManager:
    def __init__(self, env, conf):
        self.env = env
        self.conf = conf

    def __iter__(self):
        for b in self.browsers:
            yield b

    def latest(self):
        sessions_raw = map(lambda b : b.pull(), self.browsers)
        sessions = list(filter(lambda s : s is not None, sessions_raw))
        if len(sessions) == 0:
            return None
        else:
            sessions.sort(reverse=True)
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
        #if self.env.is_windows:
        #    from dokonico.browser import ie
        #    yield ie.IEFactory(self.env)

