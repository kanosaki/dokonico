
import os
import pickle

from dokonico.core import config_item
from dokonico.remote import common

class Dropbox(common.Remote):
    def __init__(self, env, conf):
        self.env = env
        self.conf = self.create_conf(env, conf)
        
    def push(self, cookie):
        with open(self.conf.session_file_path, 'wb') as f:
            pickle.dump(cookie, f)

    def pull(self):
        with open(self.conf.session_file_path, 'rb') as f:
            return pickle.load(f)

    def create_conf(self, env, root_conf):
        return DropboxConfig(env, root_conf)

class DropboxConfig:
    def __init__(self, env, root_config):
        self.root = root_config
        self.conf = root_config.dropbox

    @config_item
    def target_dir(self):
        raw_expr = self.conf["dir"]
        return raw_expr.replace("~", self.env.homedir)

    @property
    def session_file_name(self):
        return "session.dat"

    @config_item
    def session_file_path(self):
        return os.path.join(self.target_dir, self.session_file_name)

        
        
        
        
