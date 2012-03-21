
import os
import pickle
import logging
log = logging.getLogger("remote.dropbox")

from dokonico.core import config_item
from dokonico.remote import common

class Dropbox(common.Remote):
    name = "Dropbox"
    def __init__(self, env, conf):
        self.env = env
        self.conf = self.create_conf(env, conf)

    def _check_dirs(self, path):
        dir_path = os.path.dirname(path)
        if os.path.exists(dir_path):
            return True
        elif self.conf.auto_dir_create:
            os.mkdir(dir_path)
        else:
            return False
        
    def push(self, cookie):
        log.info("Pushing to Dropbox..")
        path = self.conf.session_file_path
        if not self._check_dirs(path):
            raise IOError("Dropbox sync dir not found. {}".format(os.path.dirname(path)))
        with open(path, 'wb') as f:
            pickle.dump(cookie, f)

    def pull(self):
        log.info("Pulling from Dropbox.")
        path = self.conf.session_file_path
        if not os.path.exists(path):
            return None
        with open(path, 'rb') as f:
            return pickle.load(f)

    def create_conf(self, env, root_conf):
        return DropboxConfig(env, root_conf)

class DropboxConfig:
    def __init__(self, env, root_config):
        self.env = env
        self.root = root_config
        self.conf = root_config.dropbox

    @config_item("/dropbox/dir")
    def target_dir(self):
        raw_expr = self.conf["dir"]
        return raw_expr.replace("~", self.env.homedir)

    @config_item("/dropbox/auto_dir_create")
    def auto_dir_create(self):
        return self.conf.get("auto_dir_create") or True

    @property
    def session_file_name(self):
        return "session.dat"

    @config_item("Internal")
    def session_file_path(self):
        return os.path.join(self.target_dir, self.session_file_name)

        
