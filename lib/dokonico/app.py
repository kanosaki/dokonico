
import sys
import logging as log

import dokonico.browser
import dokonico.remote

class App:
    def __init__(self, conf, env, opts):
        self.conf = conf
        self.env = env
        self.opts = opts
        
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


class Syncer(App):
    def __init__(self, conf, env, opts):
        App.__init__(self, conf, env, opts)

    def _local_latest(self):
        return self.browsers.latest()

    def _pull_remote(self):
        return self.remotes.pull()

    def _push_remote(self, cookie):
        self.remotes.push(cookie)

    @property
    def targets(self):
        for b in self.browsers:
            yield b
        yield self.remotes.current

    def _fetch_sessions(self):
        for t in self.targets:
            yield (t.pull(), t)
        
    def start(self):
        log.info("Syncing started.")
        sess_tuples = list(self._fetch_sessions())
        latest = max(sess_tuples, key=lambda t: t[0])
        latest_cookie = latest[0]
        latest_prov = latest[1]
        for (cookie, prov) in sess_tuples:
            if cookie is latest_cookie:
                continue
            log.debug("Pusing {} to {}".format(cookie, prov.name))
            prov.push(latest_cookie)

class SessionsPrinter(App):
    def __init__(self, conf, env, opts):
        App.__init__(self, conf, env, opts)
        self._load_options(opts)

    def _load_options(self, opts):
        try:
            self.out = opts.out
        except AttributeError:
            self.out = sys.stdout

    def print(self, *args, indent=0, **kw):
        print("    "* indent, *args, file=self.out, **kw)
        
    def start(self):
        print = self.print
        print("Browsers:")
        self._show_browsers()
        print("Remotes:")
        self._show_remote()

    def _show_browsers(self):
        for b in self.browsers:
            self.print(b.name + ":", indent=1)
            sess = b.pull()
            self.print(repr(sess), indent=2)

    def _show_remote(self):
        remote = self.remotes.current
        self.print(remote.name + ": ", indent=1, end="")
        sess = remote.pull()
        if sess is not None:
            self.print("(from {})".format(sess.identifier))
        else:
            self.print()
        self.print(repr(sess), indent=2)

