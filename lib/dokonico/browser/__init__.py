
class BrowserManager:
    def __init__(self):
        pass

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
            self._browsers = list(self._enumerate_browsers())
            return self._browsers

    def _enumerate_browsers(self):
        from dokonico.browser import chrome
        from dokonico.browser import firefox
        yield chrome.Chrome()
        yield firefox.Firefox()
