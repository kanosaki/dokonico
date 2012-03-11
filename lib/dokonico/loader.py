
import os

APP_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

import dokonico.env
import dokonico.core

class AppLoader:
    def __init__(self, conf="etc/config.json"):
        self.conf_path = conf

    def config(self):
        path = os.path.join(APP_ROOT, self.conf_path)
        return dokonico.core.Config(path)

    def env(self):
        factory = dokonico.env.EnvHelperFactory()
        return factory.create()

    def load(self):
        return dokonico.core.App(self.config(), self.env())
