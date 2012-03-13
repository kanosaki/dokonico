
import sys

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
            self._browser_manager = dokonico.browser.BrowserManager(
                    self.env, self.conf)
            return self._browser_manager

    @property
    def remotes(self):
        try:
            return self._remote_manager
        except AttributeError:
            self._remote_manager = dokonico.remote.RemoteManager(
                    self.env, self.conf)
            return self._remote_manager

    def _local_latest(self):
        return self.browsers.latest()

    def _pull_remote(self):
        return self.remotes.pull()

    def _push_remote(self, cookie):
        self.remotes.push(cookie)

    def show_sessions(self):
        printer = SessionsPrinter(self, {})
        printer.start()


    def sync_latest(self):
        local_latest = self._local_latest()
        remote_latest = self._pull_remote()
        if local_latest.is_newer_than(remote_latest):
            self._push_remote(local_latest)
            self.browsers.push_all(local_latest)
        else:
            self.browsers.push_all(remote_latest)


class SessionsPrinter:
    def __init__(self, app, opts):
        self.app = app
        self._load_options(opts)

    def _load_options(self, opts):
        self.out = opts.get("out") or sys.stdout

    def print(self, *args, indent=0):
        print("    "* indent, *args, file=self.out)
        
    def start(self):
        print = self.print
        print("Browsers:")
        self._show_browsers()
        print("Remotes:")
        self._show_remote()

    def _show_browsers(self):
        for b in self.app.browsers:
            self.print(b.name + ":", indent=1)
            sess = b.session()
            self.print(repr(sess), indent=2)

    def _show_remote(self):
        remote = self.app.remotes.current
        self.print(remote.name + ":", indent=1)
        sess = remote.pull()
        self.print(repr(sess), indent=2)

