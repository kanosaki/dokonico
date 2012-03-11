
import dokonico.browser
import dokonico.remote

class App:
    def __init__(self, conf, env):
        self.conf = conf
        self.env = env
        
    @property
    def browsers(self):
        try:
            return self._browser_manager
        except AttributeError:
            self._browser_manager = dokonico.browser.BrowserManager()
            return self._browser_manager

    @property
    def remotes(self):
        try:
            return self._remote_manager
        except AttributeError:
            self._remote_manager = dokonico.remote.RemoteManager()
            return self._remote_manager

    def _local_latest(self):
        return self.browsers.latest()

    def _pull_remote(self):
        return self.remotes.pull()

    def _push_remote(self, cookie):
        self.remotes.push(cookie)

    def sync_latest(self):
        local_latest = self._local_latest()
        remote_latest = self._pull_remote()
        if local_latest.is_newer_than(remote_latest):
            self._push_remote(local_latest)
            self.browsers.push_all(local_latest)
        else:
            self.browsers.push_all(remote_latest)

