
import os

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

import dokonico.env
import dokonico.browser
import dokonico.config
import dokonico.remote

class AppLoader:
    def __init__(self, conf="etc/config.json"):
        pass

    def env(self):
        factory = dokonico.env.EnvHelperFactory()
        return factory.create()

    def browsers(self):
        manager = dokonico.browser.BrowserManager()
        return manager

    def remotes(self):
        manager = dokonico.remote.RemoteManager()
        return manager

    def load(self):
        pass
